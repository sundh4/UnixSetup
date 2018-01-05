#!/bin/bash

if [ -L $0 ] ; then
    DIR=$(dirname $(readlink -f $0))
else
    DIR=$(dirname $0)
fi

"$DIR/stopPeer.sh"

NOWDATE=`date +%d%b%Y_%H%M`
/bin/mv /var/log/tomcat7/catalina.out "/var/log/tomcat7/catalina.out.restart.$NOWDATE" > /dev/null 2>&1

"$DIR/startPeer.sh"
