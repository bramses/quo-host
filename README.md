podcast host.

use speech transcription to semantic search a DB of quotes in real time. then use an llm to highlight the relevant parts of quotes that fit the transcription

![Screenshot 2024-03-22 08-48-21](https://github.com/bramses/quo-host/assets/3282661/64637cb6-398b-4d41-84ae-b4f46f0ac936)


[playlist of videos created with quo-host](https://www.youtube.com/watch?v=uzgANp2keR4&list=PLrWFPxfKMmzU2643uFacbAS8ViaGkUOLy)

## Process

Start poetry shell with `poetry shell`


1. Take edited audio file and transcribe it to text with `transcriber/transcribe_assemblyai.py` by changing `FILE_URL`
2. The transcribed json will be stored as `transcript.json`
3. Run the AI process with `transcriber/simulate.py` with `simulate_transcription_process_from_json('transcript.json')`
4. AI processed result will be stored in `logs/` folder
4a. Get missing covers with `transcriber/extract_covers.py` and edit `LOG_FILE`
5. in `public/index.html` change `log_file_path` `timestamp_file_path` and `audio_file_path` (audio needs to also be in `public/` folder)
6. check for missing covers in `transcriber/covers.json`
7. start the python server with `python server.py`
8. start the node server with `npm start`
9. open `localhost:3000` in your browser
10. click on the play button to start the audio and see the highlights (3s delay w/ stopgap solution)


Run OBS in 1080p and use the browser source to show the highlights on the screen:
```sh
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:3000
```
then in menu bar Chrome > services > resize1080p

11. `ctrl-c` to stop the servers
12. get the chapters from `transcriber/transcript_to_chapters.py` and edit `TRANSCRIPT_PATH`
