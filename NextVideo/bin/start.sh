#!/bin/bash
# !/bin/bash -x to turn echo on

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${DIR}/..

# Start the flask server
# host=0.0.0 needed to allow access from any source IP
FLASK="python3 -m flask run --host=0.0.0"

# Start the flask server in the background
echo "Starting FLASK server - server for JSON API"
# Thought that I may need to use nohup in front of server start commands - but it doesn't appear that I do
${FLASK}&
FLASK_PID=$! 


# Starting the web-server 
# NOTE: using npm - local-web-server see https://www.npmjs.com/package/local-web-server
echo "Starting Web server - for UI"
cd UI
ws&
WS_PID=$!

cd ../bin
# Create a stop.sh script to kill the running instances
echo "#!/bin/bash" > stop.sh
chmod +x stop.sh
echo "# this script is automatically created - from start.sh"
echo "kill -9 ${FLASK_PID}" >> stop.sh
echo "kill -9 ${WS_PID}" >> stop.sh
echo "***********************"
echo "run ${DIR}/stop.sh to stop the servers"
