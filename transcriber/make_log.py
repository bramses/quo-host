import uuid
import datetime
import json
import os


def create_run():
    empty_run = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.datetime.now().isoformat(),
        "quotes_shown": [],
        "what_happened": []
    }
    return empty_run

def add_step(run, step_name, data):
    step = {
        "name": step_name,
        "data": data,
        "timestamp": datetime.datetime.now().isoformat()
    }
    run["what_happened"].append(step)
    return run

def package_run(run):
    return {
        "id": run["id"],
        "created_at": run["created_at"],
        "quotes_shown": run["quotes_shown"],
        "what_happened": run["what_happened"],
        "ended_at": datetime.datetime.now().isoformat()
    }

def add_quote_shown(run, quoteId):
    run["quotes_shown"].append(quoteId)
    return run


def write_to_log(run, run_id=None):
    if run_id:
        with open(f'transcriber/logs/log-{run_id}.json', 'a') as file:
            # write to json file
            json.dump(run, file, indent=4)
        return run
    else:
        with open(f'transcriber/logs/log-{run["id"]}.json', 'a') as file:
            # write to json file
            json.dump(run, file, indent=4)
        return run
    

def read_log():
    # read latest log in transcriber/logs
    # return as json
    logs = os.listdir('transcriber/logs')
    logs.sort()
    latest_log = logs[-1]
    with open(f'transcriber/logs/{latest_log}', 'r') as file:
        return json.load(file)
    return None

def read_log_by_id(id):
    # read log by id
    logs = os.listdir('transcriber/logs')
    logs.sort()

    for log in logs:
        with open(f'transcriber/logs/{log}', 'r') as file:
            data = json.load(file)
            if data['id'] == id:
                return data
    return None

