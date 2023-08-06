#  Copyright (c) 2020 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

from abc import ABC, abstractmethod
from collections import Callable
from typing import Dict

from dlds import DLDSClient


class DLDSModel(ABC):
    def __init__(self, dlds_client: DLDSClient, model: Dict, iterations: int, iteration_callback: Callable) -> None:
        super().__init__()
        self.dlds_client = dlds_client
        self.model = model
        self.iterations = iterations
        self.iteration_callback: Callable = iteration_callback

    @abstractmethod
    def run(self) -> Dict:
        """
        Stub for implementing the training and evaluation loop. After each iteration, the iteration callback must be
        called:
        >>> self.iteration_callback(current_iteration)

        When finishing (or stopping) the training and evaluation loop, return a dictionary that contains the number of
        the current iteration, for example:

        >>> result = {
        >>>     'start_iteration': start_iteration
        >>>     'last_iteration': last_iteration
        >>> }

        :return Dictionary containing the number of iterations.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stub for stopping model training and evaluation.
        """
        pass
