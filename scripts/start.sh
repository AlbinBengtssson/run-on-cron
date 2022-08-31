#!/bin/bash
set -e

if [ $# -eq 3 ]
    then
        docker run -d "run-on-cron_run-on-cron" "$1" "$2" "$3"
        CONTAINER_ID=`docker ps -aql`
        docker cp "$2" "$CONTAINER_ID:/code/"
elif [ $# -eq 2 ]
    then
        docker run -d "run-on-cron_run-on-cron" "$1" "$2"
else
    echo "Please enter 2 or 3 input arguments. No more, no less."
fi

