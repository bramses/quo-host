'''

given a transcript, split it into yt chapters
{
    "paragraphs": [
        {
            "text": "Dear viewer, here's some food for thought. You should delete your social media profiles once a year or so. If this suggestion shocks or angers you, pause for a moment and sit with this feeling. This is a great opportunity to reflect on your relationship with social media. An annual deletion is not an argument to step away permanently.",
            "start": 320,
            "end": 21274,
        },
        ...
    ]
}

first step is to join all the paragraphs into one string
second step is to use gpt-4 to split the paragraphs into chapters and create short titles for each chapter
third step is to split the paragraphs into chapters based on the gpt-4 output

'''

import time
import json
from openai_utils import create_chapters_from_transcript

TRANSCRIPT_PATH = './transcriber/transcript-issue51.json'

def join_paragraphs(paragraphs):
    return ' '.join([f"({seconds_to_hms(paragraph['start'])}) {paragraph['text']}" for paragraph in paragraphs])

def seconds_to_hms(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds / 1000))

def load_transcript(transcript_path):
    with open(transcript_path, 'r') as file:
        transcript = json.load(file)
    return transcript

if __name__ == '__main__':
    transcript_path = TRANSCRIPT_PATH
    transcript = load_transcript(transcript_path)
    paragraphs = transcript['paragraphs']
    transcript_text = join_paragraphs(paragraphs=paragraphs)
    print(transcript_text)
    chapters = create_chapters_from_transcript(transcript_text)
    print(chapters)
