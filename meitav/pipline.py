import os
import json
import requests
from meitav.src.functionality.stt_api import get_transcription_from_blob_storage
from meitav.src.functionality.llm_functionality import conversation_summerizer, conversation_analyzer, conversation_classifier
from concurrent.futures import ThreadPoolExecutor
import traceback

from logs.logger import setup_logger, log_decorator, session_gid_var
logger = setup_logger()

def run_pipline(filename: str, transcription: str, gid: str):
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_summary = executor.submit(conversation_summerizer, transcription, gid)
        category = executor.submit(conversation_classifier, transcription, gid)
        future_analysis = executor.submit(conversation_analyzer, transcription, gid)

        summary = future_summary.result()
        conv_fields = future_analysis.result()
        category_ = category.result()
    GID = "".join(filename.split(".txt"))
    dict_return = {
        "GUID": GID,
        "category": category_,
        "summary": summary,
        "sentiment_customer": conv_fields['sentiment_caller'],
        "sentiment_representative": conv_fields['sentiment_representative'],
        "Reason_for_referral": conv_fields["Reason_for_referral"],
        "referral_3_party": conv_fields["referral_3_party"],
        "unusual_events": conv_fields['Unusual_events_or_behaviors'],
        "representative_level": conv_fields['representative_level'],
        "caller_satisfaction_level": conv_fields['caller_satisfaction_level'],
        "transcription": transcription,
        "service": "Meitav"
    }
    return dict_return


@log_decorator(show_args_calling=True, show_args_returning=True)
def async_pipeline_meitav(payload: dict):
    filename = payload.filename.split(".")[0]
    gid = filename
    session_gid_var.set(gid)
    try:
        logger.info(f"run_pipeline_in_background called with payload {str(filename)}", extra={'session_gid_var': session_gid_var.get()})
        # Your existing logic to process the request...
        transcription = get_transcription_from_blob_storage(filename=filename+".wav")
        res = run_pipline(filename=filename, transcription=transcription, gid=gid)

        # Prepare the URL for the other API
        url = os.getenv("MEITAV_MATRIX_OUTPUT_URL")
        print("sending post request")
        # Serialize `res` to a JSON string
        res_json = json.dumps(res, ensure_ascii=False).encode('utf-8')

        headers = {'Content-Type': 'application/json; charset=utf-8'}

        # Sending the request as binary data to ensure UTF-8 encoding
        response = requests.post(url, data=res_json, headers=headers)

        if response.status_code == 200:
            logger.info(f"finish Successfully for {filename} value with payload {res_json}", extra={'session_gid_var': session_gid_var.get()})
            print("Successfully sent the data to the other API.")
        else:
            logger.error(
                f"run_pipeline_in_background Failed to send data to the other API for {filename} value with payload {res_json}", extra={'session_gid_var': session_gid_var.get()})
            print(f"Failed to send data to the other API. Status code: {response.status_code}")

    except Exception as e:
        tb = traceback.format_exc()  # This line captures the traceback as a string
        print(f"An error occurred: {e}\n{tb}")  # You can print it to standard output
        logger.error(f"An error occurred: {e}\n{tb}", extra={'session_gid_var': session_gid_var.get()})  # Or log it as you prefer
