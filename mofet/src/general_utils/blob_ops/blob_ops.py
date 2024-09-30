import os
import sys

from dotenv import load_dotenv
from logs.logger import setup_logger, log_decorator, session_gid_var
from azure.storage.blob import BlobServiceClient

logger = setup_logger()

load_dotenv()
@log_decorator(show_args_calling=True, show_args_returning=False)
def get_file_from_blob_storage_and_save(filename: str):
    # try:
    # logger.info("gettingwav file from %s", filename)
    """Downloads WAV file from Azure Blob Storage and saves it to a local folder."""
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("MOFET_CONNECTION_STRING"))
    blob_client = blob_service_client.get_container_client(os.getenv("MOFET_CONTAINER_NAME")+os.getenv("MOFET_CONTAINER_DIRECTORY_PATH")).get_blob_client(filename)
    logger.info("got the blob client")

    # Ensure the tmp_files directory exists
    # local_path = "src/temp_folder"
    local_path = "./mofet/temp_folder"
    if not os.path.exists(local_path):
        logger.info("creating temporary directory")
        os.makedirs(local_path)

    # Define the full path for the local file
    download_file_path = os.path.join(local_path, filename)

    # Download blob and save it to the file
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
        logger.info("finish downloading into temporary directory")

    # logger.info.("returning from getting wav file from %s", filename)
    return download_file_path

    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     logger.error("Error occurred in file: {}, line no: {}, with message: {}".format(fname, exc_tb.tb_lineno, e))
