'''
simulate a "real" transcription process
'''
import time
from dotenv import load_dotenv
import os
import requests
from make_log import create_run, add_quote_shown, package_run, add_step, write_to_log
from openai_utils import choose_quote, bold_quote

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
    idx = 0
    # for each section split by ------------------- run a 5 second pause
    for section in transcript.split('-------------------'):
        # if idx >= 1:
        #     break
        print(section)
        run = create_run()
        run = add_step(run, 'transcribe', section)
        # post to the search endpoint with { query: section }
        response = requests.post(SEARCH_PATH, json={'query': section})
        response_json = response.json()
        run = add_step(run, 'search', response_json)
        # get the quotes from the response
        chosen_quote = choose_quote(response_json, section)
        run = add_step(run, 'select', chosen_quote)
        # bold the quote
        bolded_quote = bold_quote(response_json[chosen_quote['index']]['text'], section, chosen_quote['reasoning'])
        run = add_step(run, 'bold', bolded_quote)
        write_to_log(run, run_id=run['id'])
        # print(response.json())
        # time.sleep(5)
        idx += 1
        



if __name__ == '__main__':
    simulate_transcription_process()