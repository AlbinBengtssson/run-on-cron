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
    echo "There should be 2 or 3 input arguments, <command> <OPTIONAL: filepath> <cron>"
fi

# #!/bin/bash
# set -e

# if [ $# -eq 3 ] 
    # then
        # echo "Running" "$1 $2" "at cron interval" "$3"
        # exec "python3" "-u" "src/run_on_cron.py" "$1 /code/$2" "$3"
# else
    # echo "There should be 3 input arguments, <command> <file> <cron>"
# fi
