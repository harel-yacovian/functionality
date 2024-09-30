import os
import traceback
import requests
from logs.logger import setup_logger, log_decorator, session_gid_var
import azure.cognitiveservices.speech as speechsdk
from meitav.src.functionality.blob_storage import get_wav_file_from_blob_storage_and_save
from dotenv import load_dotenv
load_dotenv()
logger = setup_logger()


@log_decorator(show_args_calling=False, show_args_returning=False)
def transcribe_audio_from_file(audio_file_path):
    try:
        speech_key, service_region = os.getenv("MEITAV_SPEECH_KEY"), os.getenv("MEITAV_SERVICE_REGION")

        endpoint = f"https://{service_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=he-IL&format=detailed"
        headers = {
            'Ocp-Apim-Subscription-Key': f"{speech_key}",
            'Content-type': 'audio/wav;'
        }
        with open(audio_file_path, 'rb') as audio:
            data = audio.read()
        response = requests.post(endpoint, headers=headers, data=data)

        if response.status_code == 200:
            # logger.info(
            #     f"response after successfull transcription: {response.json()}, only transcription: {response.json()['DisplayText']}", extra={'session_gid_var': session_gid_var.get()})
            return response.json()['DisplayText']

    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error transcribing file {audio_file_path} error: {e}, traceback: {tb}", extra={'session_gid_var': session_gid_var.get()})
        raise Exception(e)


@log_decorator(show_args_calling=False, show_args_returning=False)
def delete_local_file(file_path):
    """Deletes a file from the local filesystem given its path."""
    # Check if the file exists
    try:
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            # logger.info(f"File {file_path}, has been deleted.", extra={'session_gid_var': session_gid_var.get()})
        else:
            logger.error(f"File {file_path}, does not exist", extra={'session_gid_var': session_gid_var.get()})
    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error deleting file {file_path} error: {e}, traceback: {tb}", extra={'session_gid_var': session_gid_var.get()})
        raise Exception(e)

@log_decorator(show_args_calling=False, show_args_returning=False)
def get_transcription_from_blob_storage(filename: str, debug=False):
    try:
        audio_file = get_wav_file_from_blob_storage_and_save(filename, debug=debug)
        transcription = api_transcribe_full_audio_from_file(audio_file, debug=debug)
        delete_local_file(audio_file)
        return transcription
    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        logger.error(f"Error getting translation for file {filename} error: {e}, traceback: {tb}", extra={'session_gid_var': session_gid_var.get()})
        raise Exception(e)



from pydub import AudioSegment
from tempfile import NamedTemporaryFile
@log_decorator(show_args_calling=False, show_args_returning=False)
def split_audio(file_path, segment_length_ms=59000):
    audio = AudioSegment.from_wav(file_path)
    segments = []
    start = 0
    while start < len(audio):
        end = min(start + segment_length_ms, len(audio))
        segment = audio[start:end]
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            segment.export(temp_file.name, format="wav")
            segments.append(temp_file.name)
        start = end
    return segments
@log_decorator(show_args_calling=False, show_args_returning=False)
def transcribe_audio_chunk(file_path, endpoint, headers):
    try:
        with open(file_path, 'rb') as audio:
            data = audio.read()
        response = requests.post(endpoint, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get('DisplayText', '')
        else:
            logger.error(f"POST request failed with status code {response.status_code}", extra={'session_gid_var': session_gid_var.get()})
            return ''
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error transcribing file {file_path}: {e}, traceback: {tb}", extra={'session_gid_var': session_gid_var.get()})
        return ''
@log_decorator(show_args_calling=False, show_args_returning=False)
def api_transcribe_full_audio_from_file(audio_file_path, debug=False):
    # logger.info("Starting transcription for file %s", audio_file_path, extra={'session_gid_var': session_gid_var.get()})
    try:
        speech_key = os.getenv("MEITAV_SPEECH_KEY")
        service_region = os.getenv("MEITAV_SERVICE_REGION")
        endpoint = os.getenv("MEITAV_SPEECH_SERVICE_URL_ENDPOINT")
        headers = {
            'Ocp-Apim-Subscription-Key': speech_key,
            'Content-type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
            'Accept': 'application/json;text/xml'
        }

        # Split the audio file into chunks
        chunks = split_audio(audio_file_path)

        # Transcribe each chunk
        transcriptions = []
        for chunk in chunks:
            transcription = transcribe_audio_chunk(chunk, endpoint, headers)
            transcriptions.append(transcription)

        # Combine all transcriptions
        full_transcription = ' '.join(transcriptions)
        return full_transcription

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error processing file {audio_file_path}: {e}, traceback: {tb}", extra={'session_gid_var': session_gid_var.get()})
        raise Exception(e)