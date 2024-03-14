# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# URL of the file to transcribe
# FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
FILE_URL = 'a-body-to-die-in.m4a' # i ran from root so file in root

# config = aai.TranscriptionConfig()

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(
  FILE_URL)

# for result in transcript.auto_highlights.results:
#   print(f"Highlight: {result.text}, Count: {result.count}, Rank: {result.rank}")

# print(f"Transcript: {transcript.text}")

paragraphs = transcript.get_paragraphs()
for paragraph in paragraphs:
  print('-------------------')
  print(paragraph.text)