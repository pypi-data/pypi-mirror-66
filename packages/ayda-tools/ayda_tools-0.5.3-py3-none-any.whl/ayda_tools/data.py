from . import config
from os import path, makedirs
from subprocess import check_call, CalledProcessError
import logging

logger = logging.getLogger(__name__)


def download_data(dataset: str) -> str:
    data_root = config.AYDA_DATA_PATH
    bucket = config.AYDA_DATA_BUCKET
    if not bucket or not data_root:
        return dataset

    dest_path = path.join(data_root, dataset)
    makedirs(dest_path, exist_ok=True)
    sync = "gsutil -m rsync -dr gs://{}/{} {}".format(bucket, dataset, dest_path)
    try:
        check_call(sync.split(" "))
    except CalledProcessError:
        logger.warning(
            "Could not download data, please check directory name. "
            "Also please check credentials for gcloud"
        )
    except FileNotFoundError:
        logger.warning(
            "Failed to sync data. Please check that gsutil is correctly installed"
        )

    return dest_path
