import concurrent.futures
from logs.logger import setup_logger, log_decorator, session_gid_var
from mofet.src.general_utils.utilities import *
from mofet.src.general_utils.utilities import __delete_local_file
from mofet.src.llm.llm_chat import llm_pipline

logger = setup_logger()


def run_main_pipline_middleware(filename: str, gid: str) -> None:
    session_gid_var.set(gid)
    _ = run_main_pipline_handler(filename)


def run_llm_pipline_middleware(domain: tuple, conversation_text: str, gid:str) -> dict:
    session_gid_var.set(gid)
    return run_llm_pipline(domain, conversation_text)
    pass

def run_llm_pipline(domain: tuple, conversation_text: str) -> dict:
    llm_dict_response = llm_pipline(domain, conversation_text)
    return llm_dict_response
    pass



@log_decorator(show_args_calling=True, show_args_returning=True)
def run_main_pipline_handler(filename: str) -> None:
    """
    this pipline runs the following steps:
    1. Download wav file.  (download file to temp_folder)
    2. Download json file. (extract info from it)
    3. Transcribe the wav file (return text)
    4. ** Speaker diarization.
    5. Voice sentiment analysis.
    6. run llm pipline.
    7. create payload
    8. send payload to matrix api server.
    9. send transcription to share point cloud.
    :param patient_id:
    :return: None
    """
    try:
        logger.info("run_main_pipline_handler start...", extra={'session_gid_var': session_gid_var.get()})

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_audio_file_path = executor.submit(get_wav_file_middleware, filename, session_gid_var.get())
            future_domain = executor.submit(get_domain_from_json_file_middleware, filename, session_gid_var.get())

            audio_file_path = future_audio_file_path.result()
            domain = future_domain.result()

            # Run get_speaker_diarization and get_transcribe_wav in parallel
            future_speaker_diarization = executor.submit(get_speaker_diarization_middleware, audio_file_path, session_gid_var.get())
            future_conversation_text = executor.submit(get_transcribe_wav_middleware, audio_file_path, session_gid_var.get())

            speaker_diarization = future_speaker_diarization.result()
            conversation_text = future_conversation_text.result()
            __delete_local_file(audio_file_path)

            # Run get_text_sentiment and run_llm_pipline in parallel
            future_voice_sentiment_analysis = executor.submit(get_text_sentiment_middleware, conversation_text, session_gid_var.get())
            future_llm_responses = executor.submit(run_llm_pipline_middleware, domain, conversation_text, session_gid_var.get())

            voice_sentiment_analysis = future_voice_sentiment_analysis.result()
            llm_responses = future_llm_responses.result()

        payload = create_payload(conversation_text, domain, speaker_diarization, voice_sentiment_analysis, llm_responses)
        status = send_payload(payload)
        # send_transcription_to_sharepoint(conversation_text)
        logger.info(f"Final status: {status}, payload_sent: {payload}",extra={'session_id': session_gid_var.get()} )
        return status
    except Exception as e:
        logger.exception(f"An error occurred in run_pipline_handler: {str(e)}\n{traceback.format_exc()}",
                         extra={'session_id': session_gid_var.get()})
    pass





# @log_decorator(show_args_calling=True, show_args_returning=True)
# def run_main_pipline_handler(filename: str) -> None:
#     """
#     this pipline runs the following steps:
#     1. Download wav file.  (download file to temp_folder)
#     2. Download json file. (extract info from it)
#     3. Transcribe the wav file (return text)
#     4. ** Speaker diarization.
#     5. Voice sentiment analysis.
#     6. run llm pipline.
#     7. create payload
#     8. send payload to matrix api server.
#     9. send transcription to share point cloud.
#     :param patient_id:
#     :return: None
#     """
#     try:
#
#         audio_file_path = get_wav_file(filename)
#         domain = get_domain_from_json_file(filename)
#         speaker_diarization = get_speaker_diarization(audio_file_path)
#         conversation_text = get_transcribe_wav(audio_file_path)
#         voice_sentiment_analysis = get_text_sentiment(conversation_text)
#         llm_responses = run_llm_pipline(domain, conversation_text)
#         payload = create_payload(conversation_text, domain, speaker_diarization, voice_sentiment_analysis, llm_responses)
#         # payload = {"test": "testing"}
#         status = send_payload(payload)
#         # send_transcription_to_sharepoint(conversation_text)
#         logger.info(f"Final status: {status}",extra={'session_id': session_gid_var.get()} )
#     except Exception as e:
#         logger.exception(f"An error occurred in run_pipline_handler: {str(e)}\n{traceback.format_exc()}",
#                          extra={'session_id': session_gid_var.get()})
#     pass
