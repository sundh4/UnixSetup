#!/bin/bash

# Script to start peer
#ulimit -Hn 65536
#ulimit -Sn 65536

echo 'Starting Rserve'
/usr/bin/R CMD Rserve > /dev/null 2>&1
EXIT_CODE="$?"
if [ "$EXIT_CODE" == "0" ]
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

sleep 3

echo 'Starting Tomcat'
/usr/sbin/service tomcat7 start
