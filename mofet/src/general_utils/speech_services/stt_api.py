import os
import traceback
import requests
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from logs.logger import setup_logger, log_decorator, session_gid_var
logger = setup_logger()

load_dotenv()


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
def api_transcribe_full_audio_from_file(audio_file_path):
    # logger.info("Starting transcription for file %s", audio_file_path)
    try:
        speech_key = os.getenv("MOFET_SPEECH_KEY")
        service_region = os.getenv("MOFET_SERVICE_REGION")
        endpoint = os.getenv("MOFET_SPEECH_SERVICE_URL_ENDPOINT")
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