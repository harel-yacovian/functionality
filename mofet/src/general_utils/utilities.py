import json
import os
import traceback
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from logs.logger import setup_logger, log_decorator, session_gid_var
from mofet.src.general_utils.blob_ops.blob_ops import get_file_from_blob_storage_and_save
from mofet.src.general_utils.speech_services.stt_api import api_transcribe_full_audio_from_file
from mofet.src.general_utils.speech_services.speaker_diarization import recognize_from_file
from mofet.src.general_utils.language_services.sentiment_service import sentiment_analysis_with_opinion_mining

load_dotenv()
logger = setup_logger()


@log_decorator(show_args_calling=False, show_args_returning=False)
def __delete_local_file(file_path):
    """Deletes a file from the local filesystem given its path."""
    # Check if the file exists
    try:
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
            logger.info(f"File {file_path}, has been deleted.", extra={'session_id': session_gid_var.get()})

        else:
            print(f"The file {file_path} does not exist.")
            logger.info(f"File {file_path}, does not exist", extra={'session_id': session_gid_var.get()})
    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error deleting file {file_path} error: {e}, traceback: {tb}",
                     extra={'session_id': session_gid_var.get()})
        raise Exception(e)


# @log_decorator(show_args_calling=False, show_args_returning=False)
def get_wav_file_middleware(filename: str, gid: str):
    """:returns str of the wav file path"""
    session_gid_var.set(gid)
    return get_wav_file(filename)


@log_decorator(show_args_calling=False, show_args_returning=False)
def get_wav_file(filename: str):
    """:returns str of the wav file path"""
    try:
        filename = filename + ".wav"
        return get_file_from_blob_storage_and_save(filename)
    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error get_wav_file error: {e}, traceback: {tb}", extra={'session_id': session_gid_var.get()})
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def __load_json_file(file_path) -> dict:
    """
    Load a JSON file from the local directory.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The content of the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        raise ValueError(f"Error loading JSON file: {e}")


@log_decorator(show_args_calling=False, show_args_returning=False)
def __decode_domain(encoded_str):
    """
    Decode a given encoded string using the hardcoded conversion dictionary.

    Parameters:
    encoded_str (str): The string to decode.

    Returns:
    str: The decoded string.
    """
    decode_map = {
        'mft.SharKeva.Att': ('שכר קבע', 'sachar_keva'),
        'MFT.Divuchim.Att ': ('שכר גמלאים', 'sachar_gimlaim'),
        'MFT.Gimlaim.Att': ('שכר גמלאים', 'sachar_gimlaim'),
        'MFT.Sharhova.Att': ('שכר חובה', 'sachar_hova'),
        'MFT.sharmiluim.Att': ('שכר מילואים', 'sachar_meloim'),
        'MFT.Sharovedzahal.Att': ('שכר אזרח עובד צהל', 'sachar_ezrach_oved_zahal'),
        'MFT.AshraiRagil.Att': ('אשראי', 'credit'),
        'MFT.AshraiML.Att': ('אשראי', 'credit'),
        'MFT.AshraiHarig.Att': ('אשראי', 'credit'),
        'MFT.Nofesh.Att': ('נופש', 'vacation')
    }

    # Return the decoded string if it exists in the dictionary
    return decode_map.get(encoded_str, "Unknown encoding")
    pass


# @log_decorator(show_args_calling=False, show_args_returning=False)
def get_domain_from_json_file_middleware(filename: str, gid: str) -> tuple:
    """:returns str of the xml file path"""
    session_gid_var.set(gid)
    return get_domain_from_json_file(filename)
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def get_domain_from_json_file(filename) -> tuple:
    """:returns str of the xml file path"""
    filename = filename + ".json"
    json_file_path = get_file_from_blob_storage_and_save(filename)
    json_file: dict = __load_json_file(json_file_path)
    __delete_local_file(json_file_path)
    return __decode_domain(json_file['ExternalQueueName'])
    pass


# @log_decorator(show_args_calling=False, show_args_returning=False)
def get_text_sentiment_middleware(text: str, gid: str):
    session_gid_var.set(gid)
    return get_text_sentiment(text)
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def get_text_sentiment(text):
    return sentiment_analysis_with_opinion_mining(text)
    pass


# @log_decorator(show_args_calling=False, show_args_returning=False)
def get_transcribe_wav_middleware(audio_file_path: str, gid: str):
    session_gid_var.set(gid)
    return get_transcribe_wav(audio_file_path)
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def get_transcribe_wav(audio_file_path: str):
    transcription = api_transcribe_full_audio_from_file(audio_file_path)
    return transcription
    pass


# @log_decorator(show_args_calling=False, show_args_returning=False)
def get_speaker_diarization_middleware(filename: str, gid: str):
    session_gid_var.set(gid)
    return get_speaker_diarization(filename)
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def get_speaker_diarization(filename):
    try:
        return recognize_from_file(filename=filename)
    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error get_speaker_diarization error: {e}, traceback: {tb}",
                     extra={'session_id': session_gid_var.get()})
        return "Error speaker diarization"
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def create_payload(conversation_text, domain, speaker_diarization, sentiment_analysis, llm_responses):
    payload = {
        "GUID": session_gid_var.get("GUID"),
        "domain": domain[0],
        "sub_domain": llm_responses['sub_domain'],
        "summary": llm_responses['summary'],
        "support_description": llm_responses['support_description'],
        "unusual_events": llm_responses['unusual_events'],
        "representative_level": llm_responses['representative_level'],
        "caller_satisfaction_level": llm_responses['caller_satisfaction_level'],
        "issue_resolution_status": llm_responses['issue_resolution_status'],
        "call_sentiment": sentiment_analysis,
        # "diarization": speaker_diarization,
        "transcription": conversation_text,
        "service": "Mofet"
    }
    return payload
    pass


@log_decorator(show_args_calling=True, show_args_returning=False)
def send_payload(payload):
    res_json = json.dumps(payload, ensure_ascii=False).encode('utf-8')

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    # Sending the request as binary data to ensure UTF-8 encoding
    response = requests.post(os.getenv("MOFET_MATRIX_OUTPUT_URL"), data=res_json, headers=headers)

    if response.status_code == 200:
        logger.info(
            f"run_pipeline_in_background finish Successfully for {session_gid_var.get()} value with payload {res_json}",
            extra={'session_gid_var': session_gid_var.get()})

        logger.info("Successfully sent the data to the other API.", extra={'session_id': session_gid_var.get()})
    else:
        logger.error(
            f"run_pipeline_in_background Failed to send data to the other API for {session_gid_var} value with payload {res_json}",
            extra={'session_id': session_gid_var.get()})
    return response.status_code
    pass


@log_decorator(show_args_calling=False, show_args_returning=False)
def send_transcription_to_sharepoint(trasnscription: str) -> None:
    pass
