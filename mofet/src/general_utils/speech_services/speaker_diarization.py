import os
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()


SPEECH_KEY = os.getenv("MOFET_SPEECH_KEY")
SPEECH_REGION = os.getenv("MOFET_SERVICE_REGION")
ln = os.getenv("MOFET_LANGUAGE")


def post_process_transcriptions(transcriptions):
    if not transcriptions:
        return []

    processed_transcriptions = []
    current_transcription = transcriptions[0]

    for i in range(1, len(transcriptions)):
        current = transcriptions[i]
        if current["Speaker ID"] == current_transcription["Speaker ID"]:
            current_transcription["Text"] += " " + current["Text"]
            current_transcription["Duration"] += current["Duration"]
            current_transcription["End"] = current["End"]
        else:
            processed_transcriptions.append(current_transcription)
            current_transcription = current

    processed_transcriptions.append(current_transcription)

    return processed_transcriptions


def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):
    print('Canceled event')


def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):
    print('SessionStopped event')


def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs, transcriptions: list):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcription = {
            "Offset": evt.result.offset,
            "Duration": evt.result.duration,
            "End": evt.result.offset / 10000000 + evt.result.duration / 10000000,
            "Speaker ID": evt.result.speaker_id,
            "Text": evt.result.text
        }
        transcriptions.append(transcription)
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))


def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):
    print('SessionStarted event')


def recognize_from_file(filename):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.endpoint_id = "ENDPOINT ID"
    speech_config.speech_recognition_language = ln

    # audio_config = speechsdk.audio.AudioConfig(filename="../../../temp_folder/123123123.wav")
    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=speech_config,
                                                                               audio_config=audio_config)

    transcriptions = []
    transcribing_stop = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        print('CLOSING on {}'.format(evt))
        nonlocal transcribing_stop
        transcribing_stop = True

    conversation_transcriber.transcribed.connect(
        lambda evt: conversation_transcriber_transcribed_cb(evt, transcriptions))
    conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
    conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)
    conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
    conversation_transcriber.session_stopped.connect(stop_cb)
    conversation_transcriber.canceled.connect(stop_cb)

    conversation_transcriber.start_transcribing_async()

    while not transcribing_stop:
        time.sleep(.2)

    conversation_transcriber.stop_transcribing_async()
    response = post_process_transcriptions(transcriptions)
    # print(response)
    return response


# recognize_from_file(filename="")
