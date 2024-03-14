'''
simulate a "real" transcription process
'''
import time
from dotenv import load_dotenv
import os
import requests

load_dotenv()

test_transcript_path = './transcriber/test.txt'
SEARCH_PATH = os.getenv('SEARCH_PATH')

def simulate_transcription_process():
    print('Simulating a "real" transcription process...')
    print('Loading test transcript...')
    with open(test_transcript_path, 'r') as file:
        transcript = file.read()
    print('Test transcript loaded.')
    print('Transcribing...')
    # for each section split by ------------------- run a 5 second pause
    for section in transcript.split('-------------------'):
        print(section)
        print('Simulating a 5 second pause...')
        # post to the search endpoint with { query: section }
        response = requests.post(SEARCH_PATH, json={'query': section})
        print(response.json())
        time.sleep(5)
        



if __name__ == '__main__':
    simulate_transcription_process()