#!/bin/bash

# Script to stop peer

echo 'Stopping Tomcat'
/usr/sbin/service tomcat7 stop
ps -ef | awk '/tomcat7/ && !/awk/ {print $2}' | xargs -r kill -9
sleep 3

echo 'Killing Rserve'
killall -9 Rserve 2>/dev/null
ps -ef | awk '/Rserve/ && !/awk/ {print $2}' | xargs -r kill -9
