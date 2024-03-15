# in terminal window one start node server with npm run start
# in terminal window two go into poetry env w poetry shell and start pythons server with python main.py


#!/bin/zsh

# Start node server in one terminal window
osascript -e 'tell app "Terminal" to do script "cd /Users/bram/Dropbox/PARA/Projects/quo-host; npm run start"'

# Start python server in another terminal window
osascript -e 'tell app "Terminal" to do script "cd /Users/bram/Dropbox/PARA/Projects/quo-host; poetry run python transcriber/simulate.py"'