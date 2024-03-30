'''
given a log file and a transcribe timestamp file, send quotes to the server at the correct timestamp

{
    "id": "21636ffa-5664-4657-ae15-c4c09ffdbb44",
    "created_at": "2024-03-29T23:39:44.904341",
    "quotes_shown": [
        312220699,
        41702122,
        687722070,
        687325918,
        687325913,
        254550553
    ],
    "what_happened": [
        {
            "id": "de5b0a0e-65a0-4a19-b68e-38493df30c71",
            "steps": [
                {
                    "name": "transcribe",
                    "data": "...",
                    "timestamp": "2024-03-29T23:39:44.904365"
                },
                {
                    "name": "search",
                    "data": [
                        {
                            "text": "But for those of you who might be on the fence when it comes to the idea of working to learn something new, I offer this word of encouragement: Life is much like going to the gym. The most painful part is deciding to go. Once you get past that, it\u2019s easy. There have been many days I have dreaded going to the gym, but once I am there and in motion, it is a pleasure. After the workout is over, I am always glad I talked myself into going.",
                            "title": "Rich Dad Poor Dad: What The Rich Teach Their Kids About Money - That The Poor And Middle Class Do Not!",
                            "similarity": 0.842152492479173,
                            "id": 41702122,
                            "author": "Robert T. Kiyosaki",
                            "thoughts": null
                        },
                        {
                            "text": "It had been more comforting to imagine that I might eventually \u201coptimize\u201d myself into the kind of person who could confront such decisions without fear, feeling totally in charge of the process. I didn\u2019t want to accept that this was never going to happen\u2014that fear was part of the deal, and that experiencing it wouldn\u2019t destroy me.",
                            "title": "Four Thousand Weeks: Time Management for Mortals",
                            "similarity": 0.837616610292174,
                            "id": 312220699,
                            "author": "Oliver Burkeman",
                            "thoughts": null
                        },
                        {
                            "text": "Life becomes a \u201cme against it\u201d situation. When you have fear, insecurity, or weakness inside of you, and you attempt to keep it from being stimulated, there will inevitably be events and changes in life that challenge your efforts. Because you resist these changes, you feel that you are struggling with life.",
                            "title": "The Untethered Soul: The Journey Beyond Yourself",
                            "similarity": 0.836041626064411,
                            "id": 41702514,
                            "author": "Michael A. Singer",
                            "thoughts": null
                        }
                    ],
                    "timestamp": "2024-03-29T23:39:47.919143"
                },
                {
                    "name": "filter",
                    "data": [
                        {
                            "text": "But for those of you who might be on the fence when it comes to the idea of working to learn something new, I offer this word of encouragement: Life is much like going to the gym. The most painful part is deciding to go. Once you get past that, it\u2019s easy. There have been many days I have dreaded going to the gym, but once I am there and in motion, it is a pleasure. After the workout is over, I am always glad I talked myself into going.",
                            "title": "Rich Dad Poor Dad: What The Rich Teach Their Kids About Money - That The Poor And Middle Class Do Not!",
                            "similarity": 0.842152492479173,
                            "id": 41702122,
                            "author": "Robert T. Kiyosaki",
                            "thoughts": null
                        },
                        {
                            "text": "It had been more comforting to imagine that I might eventually \u201coptimize\u201d myself into the kind of person who could confront such decisions without fear, feeling totally in charge of the process. I didn\u2019t want to accept that this was never going to happen\u2014that fear was part of the deal, and that experiencing it wouldn\u2019t destroy me.",
                            "title": "Four Thousand Weeks: Time Management for Mortals",
                            "similarity": 0.837616610292174,
                            "id": 312220699,
                            "author": "Oliver Burkeman",
                            "thoughts": null
                        },
                        {
                            "text": "Life becomes a \u201cme against it\u201d situation. When you have fear, insecurity, or weakness inside of you, and you attempt to keep it from being stimulated, there will inevitably be events and changes in life that challenge your efforts. Because you resist these changes, you feel that you are struggling with life.",
                            "title": "The Untethered Soul: The Journey Beyond Yourself",
                            "similarity": 0.836041626064411,
                            "id": 41702514,
                            "author": "Michael A. Singer",
                            "thoughts": null
                        }
                    ],
                    "timestamp": "2024-03-29T23:39:47.919154"
                },
                {
                    "name": "select",
                    "data": {
                        "index": 1,
                        "reasoning": "The quote about accepting fear as part of the process resonates with the speaker's fear and fragility in relation to working out and mortality, making it a relevant and thought-provoking insight."
                    },
                    "timestamp": "2024-03-29T23:39:49.049293"
                },
                {
                    "name": "bold",
                    "data": "It had been more comforting to imagine that I might eventually \u201coptimize\u201d myself into **the kind of person who could confront such decisions without fear, feeling totally in charge of the process.** **I didn\u2019t want to accept that this was never going to happen\u2014that fear was part of the deal, and that experiencing it wouldn\u2019t destroy me.**",
                    "timestamp": "2024-03-29T23:39:50.819945"
                }
            ],
            "timestamp": "2024-03-29T23:39:44.904363"
        },...
    ]
}

[{
        "text": "...",
        "start": 2760,
        "end": 20274
},...]

we can use a zip to move through the timestamps and the quotes in parallel

post to response = requests.post('http://localhost:3000/new-quote-data', json={'text': bolded_quote, 'author': filtered_quotes[chosen_quote['index']]['author'], 'title': filtered_quotes[chosen_quote['index']]['title']}) at the start of the timestamp
'''
import requests
import time
import json


def send_quotes_to_server(log_file, timestamp_file):
    timer = 0
    for log, timestamp in zip(log_file['what_happened'], timestamp_file):
        # set timer to timestamp in timestamp file using sleep
        print(f'waiting for time: {timestamp["start"] / 1000}')
        time.sleep(timestamp['start'] / 1000 - timer)
        timer = timestamp['start'] / 1000
        print(f'sending quote at time: {timestamp["start"] / 1000}')
        # filter the bolded quote from the log
        for step in log['steps']:
            if step['name'] == 'bold':
                bolded_quote = step['data']
                break
        # get the chosen quote from the log
        for step in log['steps']:
            if step['name'] == 'select':
                chosen_quote = step['data']
                break
        # get the filtered quotes from the log
        for step in log['steps']:
            if step['name'] == 'filter':
                filtered_quotes = step['data']
                break
        
        response = requests.post('http://localhost:3000/new-quote-data', json={'text': bolded_quote, 'author': filtered_quotes[chosen_quote['index']]['author'], 'title': filtered_quotes[chosen_quote['index']]['title'], 'reasoning': chosen_quote['reasoning']})

if __name__ == '__main__':
    log_file_path = "transcriber/logs/log-6007c2db-feed-43fd-9204-33e277e6a07b.json"
    timestamp_file_path = "transcriber/transcript-0329.json"

    with open(log_file_path, 'r') as log_file:
        log_file = json.load(log_file)
    with open(timestamp_file_path, 'r') as timestamp_file:
        timestamp_file = json.load(timestamp_file)

    send_quotes_to_server(log_file, timestamp_file)

