podcast host.

use speech transcription to semantic search a DB of quotes in real time. then use an llm to highlight the relevant parts of quotes that fit the transcription

![Screenshot 2024-03-22 08-48-21](https://github.com/bramses/quo-host/assets/3282661/64637cb6-398b-4d41-84ae-b4f46f0ac936)


[video of e2e run with quotes, highlighting and audio](https://www.youtube.com/watch?v=7aBJNDnoTGU)

## Process

Start poetry shell with `poetry shell`


1. Take edited audio file and transcribe it to text with `transcriber/transcribe_assemblyai.py` by changing `FILE_URL`
2. The transcribed json will be stored as `transcript.json`
3. Run the AI process with `transcriber/simulate.py` with `simulate_transcription_process_from_json('transcript.json')`
4. AI processed result will be stored in `logs/` folder
5. in `public/index.html` change `log_file_path` `timestamp_file_path` and `audio_file_path`
6. check for missing covers in `transcriber/covers.json`
7. start the python server with `python server.py`
8. start the node server with `npm start`
9. open `localhost:3000` in your browser
10. click on the play button to start the audio and see the highlights