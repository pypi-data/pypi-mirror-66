#  Copyright (c) 2019 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

import logging
import click
import dlds


@click.group()
def cli():
    pass


@cli.command('export')
@click.option('-o', '--output_dir', 'output_dir', required=True, help='Output directory.',
              type=click.Path(exists=False, file_okay=False))
@click.option('-i', '--id', 'dataset_id', required=False, default=-1, help='ID of the dataset to download.', type=int,
              prompt='Please enter the ID of the dataset to download')
@click.option('-n', '--n_items', required=False, default=-1,
              help='Number of items to download. Download all items: \'-1\'', show_default=True, type=int)
@click.option('--status', 'accepted_status', required=False, multiple=True,
              type=click.Choice(['', 'uploaded', 'annotated', 'reviewed', 'ignored']),
              help='Download only those dataset items with the given status.')
@click.option('--http_retries', required=False, default=10, help='Number of HTTP retries.', show_default=True, type=int)
@click.option('--parallel_requests', required=False, default=16, help='Number of parallel requests.', show_default=True,
              type=int)
@click.option('--username', prompt='Username', help='Username for data spree vision platform.')
@click.option('--password', prompt='Password', hide_input=True, help='Password for data spree vision platform.')
@click.option('--url', 'api_url', default='https://api.vision.data-spree.com/api',
              help='URL to the API of the platform.')
def export_command(output_dir, dataset_id, n_items, accepted_status, username, password, http_retries,
                   parallel_requests, api_url):
    dlds_client = dlds.DLDSClient(username, password, None, http_retries, parallel_requests, api_url)

    if len(accepted_status) == 0:
        accepted_status = None
    return dlds_client.download_dataset(output_dir, dataset_id, n_items, accepted_status)


@cli.command(name='import')
@click.option('--format', 'dataset_format', type=click.Choice(['dlds', 'kitti', 'coco', 'class_subdirs']), default='dlds',
              help='Dataset format to import')
@click.option('--dataset_name', help='Name of the newly created dataset.')
@click.option('--dataset_id', type=int, default=-1,
              help='ID of the dataset to which new items should be imported. If set to \'-1\', a new dataset will be created')
@click.option('--images', 'images', required=False, type=click.Path(exists=True),
              help='Directory containing the images to import.')
@click.option('--annotations', 'annotations', required=False, type=click.Path(exists=True),
              help='Directory or file containing the annotations to import.')
@click.option('--directory', 'directory', required=False, type=click.Path(exists=True),
              help='Directory or file containing data to import (only used for importing classification data from subdirectories).')
@click.option('--http_retries', required=False, default=10, help='Number of HTTP retries.', show_default=True, type=int)
@click.option('--parallel_requests', required=False, default=16, help='Number of parallel requests.', show_default=True,
              type=int)
@click.option('--username', prompt='Username', help='Username for data spree vision platform.')
@click.option('--password', prompt='Password', hide_input=True, help='Password for data spree vision platform.')
@click.option('--url', 'api_url', default='https://api.vision.data-spree.com/api',
              help='URL to the API of the platform.')
def import_command(dataset_format, dataset_id, dataset_name, images, annotations, directory, http_retries,
                   parallel_requests, username, password,
                   api_url):
    dlds_client = dlds.DLDSClient(username, password, None, http_retries, parallel_requests, api_url)
    if dataset_format == 'dlds':
        return dlds_client.import_dlds(dataset_name, dataset_id, images, annotations)
    elif dataset_format == 'kitti':
        return dlds_client.import_kitti(dataset_name, dataset_id, images, annotations)
    elif dataset_format == 'coco':
        return dlds_client.import_coco(dataset_name, dataset_id, images, annotations)
    elif dataset_format == 'class_subdirs':
        return dlds_client.import_classification_directories(dataset_name, dataset_id, directory)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)-6s %(message)s')
    cli()
