# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# URL of the file to transcribe
# FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
FILE_URL = 'issue50.mp3'  # i ran from root so file in root
print("Transcribing file at URL: ", FILE_URL)
# config = aai.TranscriptionConfig()

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(
    FILE_URL)

print("Transcription complete.")
print("Getting paragraphs...")
json_obj_paragraphs = []
paragraphs = transcript.get_paragraphs()
for paragraph in paragraphs:
    paragraph_text = paragraph.text
    # get start and end time of the paragraph
    paragraph_start = paragraph.start
    paragraph_end = paragraph.end

    # print(f"Paragraph: {paragraph_text}")
    # print(f"Start: {paragraph_start}, End: {paragraph_end}")

    words = []
    for word in paragraph.words:
        word_text = word.text
        word_start = word.start
        word_end = word.end
        word_confidence = word.confidence

        words.append({
            "text": word_text,
            "start": word_start,
            "end": word_end,
            "confidence": word_confidence
        })

    json_obj_paragraphs.append({
        "text": paragraph_text,
        "start": paragraph_start,
        "end": paragraph_end,
        "words": words
    })

# [Word(text='Smoke', start=250, end=650, confidence=0.73033), Word(text='from', start=730, end=1022, confidence=0.99996), ...]
# convert the words to json
print("Getting words...")
json_obj_words = []
for word in transcript.words:
    word_text = word.text
    word_start = word.start
    word_end = word.end
    word_confidence = word.confidence

    json_obj_words.append({
        "text": word_text,
        "start": word_start,
        "end": word_end,
        "confidence": word_confidence
    })

print("Writing to transcript.json...")
json_obj = {
    "paragraphs": json_obj_paragraphs,
    "words": json_obj_words
}

json_obj = json.dumps(json_obj, indent=4)
with open('transcript.json', 'w') as file:
    file.write(json_obj)
