'''
simulate a "real" transcription process
'''
import time
from dotenv import load_dotenv
import os
import requests
from make_log import add_quote_shown, package_run, add_step, write_to_log, add_process
from openai_utils import choose_quote, bold_quote

load_dotenv()

SEARCH_PATH = os.getenv('SEARCH_PATH')
RANDOM_PATH = os.getenv('RANDOM_PATH')

# run = create_run()


def process(transcript, run):
    try:
        run = add_process(run)
        process_id = run['what_happened'][-1]['id']

        
        run = add_step(run, 'transcribe', process_id, transcript)
        # post to the search endpoint with { query: transcript }
        response = requests.post(SEARCH_PATH, json={'query': transcript})
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

        chosen_quote = choose_quote(filtered_quotes, transcript)
        run = add_step(run, 'select', process_id, chosen_quote)
        # add quote id to quotes_shown
        run = add_quote_shown(run, filtered_quotes[chosen_quote['index']]['id'])
        # bold the quote
        bolded_quote = bold_quote(filtered_quotes[chosen_quote['index']]['text'], transcript, chosen_quote['reasoning'])
        run = add_step(run, 'bold', process_id, bolded_quote)
        # post to http://localhost:3000/new-quote-data with { text: bolded_quote, author: response_json[chosen_quote['index']]['author'], title: response_json[chosen_quote['index']]['title'] }
        response = requests.post('http://localhost:3000/new-quote-data', json={'text': bolded_quote, 'author': filtered_quotes[chosen_quote['index']]['author'], 'title': filtered_quotes[chosen_quote['index']]['title']})

        return run
        # print(response.json())
    except Exception as e:
        print(e)
        run = package_run(run)
        write_to_log(run, run_id=run['id'])
        print('Error occurred, writing to log...')
        print('Exiting...')
        return run

        



if __name__ == '__main__':
    simulate_transcription_process()