#!/bin/bash

#
# Configuration system
#
DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PORT=$1
NAMESPACE=$2
TIMEOUT=$3
ID=$4
FILE_PID="${DIRECTORY}/${ID}.pid"
FILE_JAR="${DIRECTORY}/${ID}.jar"
URL_TASK="http://localhost:${PORT}/${NAMESPACE}/task/detail/${ID}.txt"
URL_READY="http://localhost:${PORT}/${NAMESPACE}/task/update/${ID}.txt"
CAN_RUN=1
INFO="Nothing abnormal"

$(cd $DIRECTORY)
WHOAMI=$(whoami)
DETAIL=$(curl -s $URL_TASK)
TASK=$(echo $DETAIL | awk -F "\"* // \"*" '{print $1}' | cut -d ':' -f 2)
UPDATE=$(curl -sc $FILE_JAR $URL_READY)
TOKEN=$(echo $UPDATE | awk -F "\"* // \"*" '{print $4}' | cut -d ':' -f 2)

echo $TASK

if [ -f $FILE_PID ]; then
    CONTENT_FILE_PID=$(cat $FILE_PID)
    PIDPROC=$(ps aux | grep "$CONTENT_FILE_PID" | grep -v "grep" | wc -l)
    if [ $PIDPROC -gt 0 ]; then
        UP_TIME=$(ps -u $WHOAMI -o etimes,cmd | grep "$TASK" | awk '{print $1}' | head -n1)
        if [ $UP_TIME -gt $TIMEOUT ]; then
            $(kill -9 $CONTENT_FILE_PID > /dev/null)
            $(rm $FILE_PID)
            echo "test"
            INFO="A task was killed"
        else
            CAN_RUN=0
            ERROR="A task is already progress"
        fi
    fi
fi

if [ $CAN_RUN -eq 1 ] ; then
    SCRIPTPROC=$(ps aux | grep "${TASK}.py" | grep -v "grep" | wc -l)
    if [ $SCRIPTPROC -gt 0 ]; then
        ALLPROC=$(ps -ewo pid,etimes,cmd | grep "${TASK}.py" | grep -v "grep")
        while read pid etimes cmd
        do
            if [ "$etimes" -gt $TIMEOUT ]; then
                if [ $STATUS == 1 ]; then
                    $(kill -9 $pid > /dev/null)
                    if [ $SCRIPTPROC -gt 1 ]; then
                        INFO="${SCRIPTPROC} were killed"
                    else
                        INFO="A task was killed"
                    fi
                fi
            fi
        done <<< "$(echo -e "$ALLPROC")"
    fi
fi

#if [ $CAN_RUN -eq 1 ] ; then
#    $(curl -sb $FILE_JAR $URL_READY -d "status=ready&info=${INFO}&error=&csrfmiddlewaretoken=${TOKEN}")
#else
#    $(curl -sb $FILE_JAR $URL_READY -d "status=error&info=&error=${ERROR}&csrfmiddlewaretoken=${TOKEN}")
#fi
$(rm $FILE_JAR)