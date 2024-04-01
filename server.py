from flask import Flask, request, jsonify
from transcriber.display_log_timestamp import send_quotes_to_server
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/send-quotes', methods=['POST'])
def send_quotes():
    print(request.json)
    log_file = request.json['log_file']
    timestamp_file = request.json['timestamp_file']
    # open the log file and timestamp file
    with open(log_file, 'r') as log_file:
        log_file = json.load(log_file)
    with open(timestamp_file, 'r') as timestamp_file:
        timestamp_file = json.load(timestamp_file)
    send_quotes_to_server(log_file, timestamp_file)
    return jsonify({'message': 'Quotes sent to server'})

# run the flask app on port 5000

if __name__ == '__main__':
    app.run(port=5000, debug=True)



