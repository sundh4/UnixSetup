#!/bin/bash

# Checker if running or not
PIDRSERVE=`ps -ef | awk '/Rserve/ && !/awk/ {print $2}'`
if [ "$PIDRSERVE" != '' ]
then
    kill -9 $PIDRSERVE
fi

# Start Rserve
/usr/bin/R CMD Rserve > /dev/null 2>&1
if [ "$?" == '0' ]
then
    STATUS="Rserve Running"
    echo "$STATUS at $(date +%F)"
    echo "$STATUS at $(date +%F)" >/var/log/rserve.log
else
    STATUS="Rserve Failed"
    echo "$STATUS at $(date +%F)"
    echo "$STATUS at $(date +%F)" >/var/log/rserve.log
    exit 2
fi
