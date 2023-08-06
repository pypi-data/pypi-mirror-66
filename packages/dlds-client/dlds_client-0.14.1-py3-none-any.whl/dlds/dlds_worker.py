#  Copyright (c) 2020 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

import asyncio
import json
import logging
import time
from asyncio import Future
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional, Awaitable, Dict, AsyncIterator, Type, Any

import aiohttp

from dlds import DLDSClient, DLDSModel

logger = logging.getLogger(__name__)


class DLDSWorker:

    def __init__(self, dlds_client, worker_id: int, model_id=None, ws_url: str = 'wss://api.vision.data-spree.com/ws',
                 keep_up=False, keep_up_time=300.0, message_wait_timeout=30.0, send_queue_max_size=10):
        super().__init__()
        self.dlds_client: DLDSClient = dlds_client
        self.dlds_models: Dict[DLDSModel] = {}
        self.worker_url: str = '{}/worker/{}'.format(ws_url, worker_id)
        self.worker_id: int = worker_id
        self.model_id: int = model_id
        self.keep_up: bool = keep_up
        self.keep_up_time: float = keep_up_time  # seconds
        self.message_wait_timeout = message_wait_timeout  # seconds

        self.current_dlds_model: Optional[DLDSModel] = None
        self.current_dlds_model_class: Optional[Type[DLDSModel]] = None
        self.current_run: Optional[Awaitable] = None
        self.current_job: Optional[Dict] = None

        self.ws = None
        self.send_queue = asyncio.Queue(maxsize=send_queue_max_size)
        self.message_waiter: Optional[Future] = None
        self.running = True
        self.pool = ThreadPoolExecutor(max_workers=2)

    def register_model(self, model_config_ids, dlds_model) -> None:
        """
        Register a DLDS Model class for the specified model config IDs. The DLDS worker is going to process models that
        have one of the registered config IDs.

        :param model_config_ids: IDs of the model configurations.
        :param dlds_model: DLDS Model class to be registered for the specified model config ID.
        """

        for model_config_id in model_config_ids:
            self.dlds_models[model_config_id] = dlds_model

    def run(self):
        """
        Start the processing loops.
        """
        loop = asyncio.get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()

        loop.run_until_complete(
            asyncio.gather(self.run_process_messages(), self.run_send_messages(), self.run_process_jobs()))

    async def run_process_jobs(self) -> None:
        """
        Fetch jobs from DLDS and start the model training / evaluation.
        """

        loop = asyncio.get_event_loop()

        job_time = time.time()

        while self.running:
            jobs = await loop.run_in_executor(self.pool, self.dlds_client.get_jobs, self.worker_id)

            self.current_job = None
            self.current_dlds_model_class = None
            model = None
            for job in jobs:

                if job['status'] == 'exception':
                    continue

                job_model_id = job['model']
                if job_model_id != self.model_id and self.model_id is not None:
                    continue

                model: Optional[Dict] = await loop.run_in_executor(self.pool, self.dlds_client.get_model, job_model_id)

                if model is None:
                    continue

                model['parameters'] = await loop.run_in_executor(self.pool, self.dlds_client.get_model_parameters,
                                                                 job_model_id)

                model_config_id = model['network_config_option']
                self.current_dlds_model_class = self.dlds_models.get(model_config_id)
                if self.current_dlds_model_class is None:
                    continue
                else:
                    # a job that can be processed by this worker has been found
                    self.current_job = job
                    break

            if self.current_dlds_model_class is not None and self.current_job is not None:
                # set up the dlds model and start it
                def iteration_callback(iteration):
                    message = {
                        'type': 'status',
                        'status': 'running',
                        'iteration': iteration,
                        'job': job,
                    }

                    logger.debug(f'Iteration callback (job: {job}, iteration: {iteration})')

                    try:
                        self.send_queue.put_nowait(message)
                    except asyncio.QueueFull as e:
                        logger.warning('Websocket sending queue is full.')

                iterations = self.current_job.get('iterations', 0)

                # create DLDS Model instance
                self.current_dlds_model = await loop.run_in_executor(self.pool, self.current_dlds_model_class,
                                                                     self.dlds_client, model, iterations,
                                                                     iteration_callback)
                self.current_run = loop.run_in_executor(self.pool, self.current_dlds_model.run)

                # block until finished
                try:
                    await loop.run_in_executor(self.pool, self.dlds_client.update_job,
                                               {'id': self.current_job['id'], 'status': 'running'})
                    result = await self.current_run
                    await loop.run_in_executor(self.pool, self.dlds_client.delete_job, self.current_job.get('id'))
                    if result is not None and result.get('last_iteration') is not None:
                        # send an update message in case the iteration should be updated
                        message = {
                            'type': 'status',
                            'status': 'stopped',
                            'iteration': result.get('last_iteration'),
                            'job': self.current_job,
                        }
                        await self.send_message(message)
                except Exception as e:
                    logger.exception(f'Error during model run: {e}')
                    await loop.run_in_executor(self.pool, self.dlds_client.update_job,
                                               {'id': self.current_job['id'], 'status': 'exception'})
                    await asyncio.sleep(1.0)

                # reset the job time so that the worker can execute some more jobs
                job_time = time.time()

            else:
                logger.info('no jobs found')
                self.message_waiter = loop.create_future()
                try:
                    await asyncio.wait_for(self.message_waiter, self.message_wait_timeout)
                except asyncio.futures.TimeoutError as e:
                    self.message_waiter.cancel()
                except Exception as e:
                    logger.exception(f'An exception occurred during waiting for messages: {e}')
                    if self.message_waiter is not None:
                        self.message_waiter.cancel()

            if not self.keep_up:
                now = time.time()
                if now - job_time > self.keep_up_time:
                    self.stop()

    async def run_send_messages(self) -> None:
        """
        Send enqueued messages via websocket.
        """
        while self.running:
            try:
                message = await asyncio.wait_for(self.send_queue.get(), timeout=1.0)
                await self.send_message(message)
            except asyncio.TimeoutError as e:
                pass

    async def run_process_messages(self) -> None:
        """
        Process incoming websocket messages and check the job that is currently running.
        """
        loop = asyncio.get_event_loop()
        websocket_connection = self.websocket_connection()

        while self.running:

            # try to fetch a message from the websocket connection
            message: Optional[Dict] = None
            try:
                message = await asyncio.wait_for(websocket_connection.__anext__(), timeout=self.message_wait_timeout)
            except StopAsyncIteration as e:
                websocket_connection = self.websocket_connection()
                continue
            except asyncio.futures.TimeoutError as e:
                pass
            except Exception as e:
                logger.exception(f'Exception during fetching websocket messages: {e}')

            # fetch job information from DLDS
            if message is None:
                if self.current_job is not None:
                    job = loop.run_in_executor(self.pool, self.dlds_client.get_job, self.current_job.get('id'))
                    if job is None:
                        message = {
                            'type': 'job_deleted',
                            'job_id': self.current_job.get('id')
                        }

            if message is not None:
                if 'type' in message and message.get('type') == 'job_deleted' and \
                        self.current_job is not None and message.get('job_id') == self.current_job.get('id'):
                    if self.current_dlds_model is not None:
                        self.current_dlds_model.stop()

                if self.message_waiter is not None:
                    if not self.message_waiter.done():
                        self.message_waiter.set_result(None)

    async def websocket_connection(self) -> AsyncIterator[Dict]:
        """
        Create a websocket connection to the worker websocket API to receive notifications about new jobs, deleted jobs
        etc., and to send status messages to DLDS, e.g. after an iteration completed.
        :return: Iterator for incoming messages.
        """
        while self.running:
            # connect via websocket to dlds
            async with aiohttp.ClientSession() as session:
                logger.debug(f'Try to connect via websocket to {self.worker_url}')
                async with session.ws_connect(self.worker_url) as ws:
                    logger.debug(f'Websocket connection established to {self.worker_url}')
                    self.ws = ws
                    async for msg in ws:
                        logger.debug(f'Received message via websockets: {msg.data}')
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            message_dict = json.loads(msg.data)
                            yield message_dict
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            logger.warning('Websocket connection error.')
                            break

                self.ws = None

                # wait a second before trying to re-connect
                await asyncio.sleep(1)

    async def send_message(self, message: Dict) -> None:
        """
        Send a message via websockets to DLDS.
        :param message: Dictionary to be serialized as json.
        """
        if self.ws:
            try:
                await self.ws.send_str(json.dumps(message))
            except Exception as e:
                logger.warning(e)

    def stop(self) -> None:
        """
        Stop the worker.
        """
        self.running = False
