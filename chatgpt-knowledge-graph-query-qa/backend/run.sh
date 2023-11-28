#!/bin/bash

IMAGE_NAME=askwiki
APP_NAME=askwiki
ASKWIKI_HOST=localhost

# stop and remove image in case this script was run before
docker stop ${APP_NAME}
docker rm ${APP_NAME}

# rebuild and run the new image
docker build -t ${IMAGE_NAME} ./${APP_NAME}/
docker run -d --name ${APP_NAME} -p 8000:8000 ${IMAGE_NAME}

# wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://$ASKWIKI_HOST:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 5
    fi
done

# check a few endpoints and their http response
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://$ASKWIKI_HOST:8000/"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://$ASKWIKI_HOST:8000/docs"

curl -o /dev/null -X POST "http://$ASKWIKI_HOST:8000/ask/" \
   -H 'Content-Type: application/json' \
   -d '{"pipeline": "dummy", "question": "what is the difference between a duck?"}'

# output and tail the logs for the container
docker logs -f ${APP_NAME}
