'''
simulate a "real" transcription process
'''
import time
from dotenv import load_dotenv
import os
import requests
from make_log import create_run, add_quote_shown, package_run, add_step, write_to_log, add_process
from openai_utils import choose_quote, bold_quote
import json

load_dotenv()

test_transcript_path = './transcriber/test.txt'
SEARCH_PATH = os.getenv('SEARCH_PATH')
RANDOM_PATH = os.getenv('RANDOM_PATH')

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
    try:
        for section in transcript.split('-------------------'):
            if idx >= 4:
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

            run = add_step(run, 'filter', process_id, filtered_quotes)
            
            # if filtered_quotes is empty, post to RANDOM_PATH to get random quotes
            if len(filtered_quotes) == 0:
                print('No quotes found, getting random quotes...')
                response = requests.post(RANDOM_PATH)
                response_json = response.json()
                for quote in response_json:
                    quote['title'] = quote['book']['title']
                    quote['author'] = quote['book']['author']
                    del quote['embedding']
                print('Random quotes:', response_json)
                run = add_step(run, 'random', process_id, response_json)
                filtered_quotes = response_json

            chosen_quote = choose_quote(filtered_quotes, section)
            run = add_step(run, 'select', process_id, chosen_quote)
            # add quote id to quotes_shown
            run = add_quote_shown(run, filtered_quotes[chosen_quote['index']]['id'])
            # bold the quote
            bolded_quote = bold_quote(filtered_quotes[chosen_quote['index']]['text'], section, chosen_quote['reasoning'])
            run = add_step(run, 'bold', process_id, bolded_quote)
            # post to http://localhost:3000/new-quote-data with { text: bolded_quote, author: response_json[chosen_quote['index']]['author'], title: response_json[chosen_quote['index']]['title'] }
            response = requests.post('http://localhost:3000/new-quote-data', json={'text': bolded_quote, 'author': filtered_quotes[chosen_quote['index']]['author'], 'title': filtered_quotes[chosen_quote['index']]['title']})
            # print(response.json())
            time.sleep(5)
            idx += 1
        run = package_run(run)
        write_to_log(run, run_id=run['id'])
    except Exception as e:
        print(e)
        run = package_run(run)
        write_to_log(run, run_id=run['id'])
        print('Error occurred, writing to log...')
        print('Exiting...')

        
def simulate_transcription_process_from_json(transcript_path='./transcriber/transcript.json'):
    print('Simulating a "real" transcription process...')
    print('Loading test transcript...')
    with open(transcript_path, 'r') as file:
        transcript = file.read()
    print('Test transcript loaded')
    json_obj = json.loads(transcript)
    '''
    [{
        "text": "...",
        "start": 2760,
        "end": 20274
    }]
    '''
    print('Transcribing...')
    run = create_run()
    for section in json_obj:
        print(section)
        run = add_process(run)
        process_id = run['what_happened'][-1]['id']
        run = add_step(run, 'transcribe', process_id, section['text'])
        # post to the search endpoint with { query: section }
        response = requests.post(SEARCH_PATH, json={'query': section['text']})
        response_json = response.json()
        run = add_step(run, 'search', process_id, response_json)
        # get the quotes from the response
        # filter out quotes that have already been shown
        filtered_quotes = [quote for quote in response_json if quote['id'] not in run['quotes_shown']]
        run = add_step(run, 'filter', process_id, filtered_quotes)

        # if filtered_quotes is empty, post to RANDOM_PATH to get random quotes
        if len(filtered_quotes) == 0:
            print('No quotes found, getting random quotes...')
            response = requests.post(RANDOM_PATH)
            response_json = response.json()
            for quote in response_json:
                quote['title'] = quote['book']['title']
                quote['author'] = quote['book']['author']
                del quote['embedding']
            print('Random quotes:', response_json)
            run = add_step(run, 'random', process_id, response_json)
            filtered_quotes = response_json

        chosen_quote = choose_quote(filtered_quotes, section['text'])
        run = add_step(run, 'select', process_id, chosen_quote)
        # add quote id to quotes_shown
        run = add_quote_shown(run, filtered_quotes[chosen_quote['index']]['id'])
        # bold the quote
        bolded_quote = bold_quote(filtered_quotes[chosen_quote['index']]['text'], section['text'], chosen_quote['reasoning'])
        run = add_step(run, 'bold', process_id, bolded_quote)

    run = package_run(run)
    write_to_log(run, run_id=run['id'])

    print('Transcription complete.')
    print('Exiting...')




if __name__ == '__main__':
    # simulate_transcription_process()
    simulate_transcription_process_from_json('./transcriber/transcript-watts.json')