#!/bin/bash
set -e

if [ $# -eq 3 ] 
    then 
    echo "Running" "$1" "$2" "at cron interval" "$3"
    exec "python3" "-u" "src/run_on_cron.py" "$1 $2" "$3"
elif [ $# -eq 2 ]
    then
    echo "Running" "$1" "at cron interval" "$2"
    exec "python3" "-u" "src/run_on_cron.py" "$1" "$2"
else
    echo "Specify command and cron interval using '--command=' and '--cron='"
    echo "For example:"
    echo docker run --rm -v '$(pwd)'/run-on-cron run-on-cron_run-on-cron --command="'"python /code/scripts/example_py_script.py"'" --cron="'""* * * * *""'"
    # exit 1
fi

# if [[ "$*" == *--command* ]] && [[ "$*" == *--cron* ]]; then
#     echo "$1"
#     ## Just run as-is
#     python3 "-u" "src/run_on_cron.py" "$@"
# else
#     ## Include standard defaultsFile
#     echo "Specify command and cron interval using '--command=' and '--cron='"
#     echo "For example:"
#     echo docker run --rm -v '$(pwd)'/run-on-cron run-on-cron_run-on-cron --command="'"python /code/scripts/example_py_script.py"'" --cron="'""* * * * *""'"
#     exit 1
# fi
