import os
from dotenv import load_dotenv
load_dotenv()

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from logs.logger import setup_logger, log_decorator, session_gid_var
logger = setup_logger()
# Load the key and endpoint from environment variables
language_key = os.environ.get('MOFET_AZURE_LANGUAGE_SERVICE_KEY')
language_endpoint = os.environ.get('MOFET_AZURE_LANGUAGE_SERVICE_URL')

# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

@log_decorator(show_args_calling=False, show_args_returning=False)
def sentiment_analysis_with_opinion_mining(text):
    
    documents = [text]

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    if doc_result:
        document = doc_result[0]
        sentiment_dict = {
            "sentiment": {
                "positive": document.confidence_scores.positive,
                "neutral": document.confidence_scores.neutral,
                "negative": document.confidence_scores.negative
            }
        }
        return sentiment_dict
    else:
        logger.error("sentiment analysis error!", extra={'session_id': session_gid_var.get()})
        return {"sentiment": "Analysis failed or returned an error."}