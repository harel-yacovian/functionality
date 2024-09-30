import os
import sys
from azure.storage.blob import BlobServiceClient
from logs.logger import setup_logger, log_decorator, session_gid_var

logger = setup_logger()

@log_decorator(show_args_calling=True, show_args_returning=False)
def get_wav_file_from_blob_storage_and_save(filename: str, debug=False):
    try:
        logger.info(f"gettingwav file from {filename}", extra={'session_gid_var': session_gid_var.get()})
        """Downloads WAV file from Azure Blob Storage and saves it to a local folder."""
        if debug:
            blob_service_client = BlobServiceClient.from_connection_string(os.getenv("MEITAV_CONNECTION_STRING"))
            blob_client = blob_service_client.get_container_client(os.getenv("MEITAV_TEST_CONTAINER_NAME")+os.getenv("MEITAV_TEST_CONTAINER_DIRECTORY_PATH")).get_blob_client(filename)
        else:    
            blob_service_client = BlobServiceClient.from_connection_string(os.getenv("MEITAV_CONNECTION_STRING"))
            blob_client = blob_service_client.get_container_client(os.getenv("MEITAV_CONTAINER_NAME")+os.getenv("MEITAV_CONTAINER_DIRECTORY_PATH")).get_blob_client(filename)

        # Ensure the tmp_files directory exists
        local_path = "./meitav/tmp_files"
        if not os.path.exists(local_path):
            # logger.info("creating temporary directory", extra={'session_gid_var': session_gid_var.get()})
            os.makedirs(local_path)

        # Define the full path for the local file
        download_file_path = os.path.join(local_path, filename)

        # Download blob and save it to the file
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
            # logger.info(f"finish downloading into temporary directory",
            #             extra={'session_gid_var': session_gid_var.get()})

        return download_file_path

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(f"Error occurred in file: {fname}, line no: {exc_tb.tb_lineno}, with message: {e}",
                    extra={'session_gid_var': session_gid_var.get()})




