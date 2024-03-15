'''
simulate a "real" transcription process
'''
import time
from dotenv import load_dotenv
import os
import requests
from make_log import create_run, add_quote_shown, package_run, add_step, write_to_log, add_process
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
    run = create_run()
    for section in transcript.split('-------------------'):
        if idx >= 2:
            break
        print(section)
        run = add_process(run)
        process_id = run['what_happened'][-1]['id']

        
        run = add_step(run, 'transcribe', process_id, section)
        # post to the search endpoint with { query: section }
        response = requests.post(SEARCH_PATH, json={'query': section})
        response_json = response.json()
        run = add_step(run, 'search', process_id, response_json)
        # get the quotes from the response
        # filter out quotes that have already been shown
        filtered_quotes = [quote for quote in response_json if quote['id'] not in run['quotes_shown']]
        chosen_quote = choose_quote(filtered_quotes, section)
        run = add_step(run, 'select', process_id, chosen_quote)
        # add quote id to quotes_shown
        run = add_quote_shown(run, response_json[chosen_quote['index']]['id'])
        # bold the quote
        bolded_quote = bold_quote(response_json[chosen_quote['index']]['text'], section, chosen_quote['reasoning'])
        run = add_step(run, 'bold', process_id, bolded_quote)
        # post to http://localhost:3000/new-quote-data with { text: bolded_quote, author: response_json[chosen_quote['index']]['author'], title: response_json[chosen_quote['index']]['title'] }
        response = requests.post('http://localhost:3000/new-quote-data', json={'text': bolded_quote, 'author': response_json[chosen_quote['index']]['author'], 'title': response_json[chosen_quote['index']]['title']})
        # print(response.json())
        time.sleep(5)
        idx += 1
    run = package_run(run)
    write_to_log(run, run_id=run['id'])

        



if __name__ == '__main__':
    simulate_transcription_process()