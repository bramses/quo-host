# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Then, make sure you have PyAudio installed: https://pypi.org/project/PyAudio/
#
# Note: Some macOS users might need to use `pip3` instead of `pip`.

import assemblyai as aai
from dotenv import load_dotenv
import os
import time

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

DRINKING_BIRD_LENGTH = 200
drinking_bird = ""


def on_open(session_opened: aai.RealtimeSessionOpened):
    "This function is called when the connection has been established."

    print("Session ID:", session_opened.session_id)


def on_data(transcript: aai.RealtimeTranscript):
    "This function is called when a new transcript has been received."

    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
        global drinking_bird
        drinking_bird += transcript.text
    else:
        print(transcript.text, end="\r")

    
    if len(drinking_bird) > DRINKING_BIRD_LENGTH:
        drinking_bird = drinking_bird[-DRINKING_BIRD_LENGTH:]
        print("filled up drinking bird")
        print(drinking_bird)
        # clear drinking bird
        drinking_bird = ""


def on_error(error: aai.RealtimeError):
    "This function is called when the connection has been closed."

    print("An error occured:", error)


def on_close():
    "This function is called when the connection has been closed."

    print("Closing Session")


transcriber = aai.RealtimeTranscriber(
    on_data=on_data,
    on_error=on_error,
    sample_rate=44_100,
    on_open=on_open,  # optional
    on_close=on_close,  # optional
)

# Start the connection
transcriber.connect()

# Open a microphone stream
microphone_stream = aai.extras.MicrophoneStream()


# Press CTRL+C to abort
transcriber.stream(microphone_stream)

transcriber.close()
