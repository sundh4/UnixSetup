#!/bin/bash

#******************************************************************************
#
# Copyright: Intellectual Property of Four Elements Capital Pte Ltd, Singapore.
# All rights reserved.
#
#******************************************************************************

# This is scripts for deploying peer
# Make sure running this script from Computer Setup main program
# If used this script separately, make sure R, Rserve, OpenJDK7 and Tomcat7
# Correctly installed and configured

# Determine path where the script running
if [ -L $0 ] ; then
	SCRIPT_PATH=$(dirname $(readlink -f $0))
else
	SCRIPT_PATH=$(dirname $0)
fi

#Check these params value first :
P2P_PARENT_FOLDER="/4EUtils/"
P2PSERVER_PATH="$P2P_PARENT_FOLDER/p2pserver"
LOG_PATH=$P2PSERVER_PATH"/logs"
ERROR_LOG_PATH="$LOG_PATH/errorlogs"
QUEUE_PATH="$P2PSERVER_PATH/queue"
#P2P_PUBLIC_FOLDER="/mnt/public/Infrastructure/Linux_Unix/Current Version/R and Peer Software/Ubuntu_Peer/p2pserver/"
P2P_PUBLIC_FOLDER="$SCRIPT_PATH/p2pserver"
#GIT_FOLDER_PATH="/Git/Applications"
GIT_PARENT_PATH="/Git"
GIT_FOLDER_PATH="$GIT_PARENT_PATH/JavaApps"
BACKUP_PARENT_PATH="/temp/peer_deploy_backup"
GITHUB_REPO_URL="https://github.com/FourElementsCapital/JavaApps.git"

set -e

v_out="$1"
key="$2"

# Arguments checker. Should be minimal 1 arg and max 2 args
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]
then
    echo "(ERROR Argument) - Usage: $0 <version> <-f or --fresh>"
    echo "<-f or --fresh> arguments are OPTIONAL"
    exit 1
fi

# Set variable fresh into FALSE mean default are not fresh installation
is_fresh="FALSE"
if [ $# -gt 1 ]
then
    case $key in
        -f|--fresh)
            is_fresh="TRUE"
            shift
            ;;
        *)
            echo "Error argument. use -f or --fresh"
            exit 1
            ;;
    esac
fi
# Initialize path and folders
SCHEDULER_REPO_PATH="$GIT_FOLDER_PATH/Scheduler"
SCHEDULER_RELEASE_PATH="$SCHEDULER_REPO_PATH/release/$v_out"
BACKUP_PATH="$BACKUP_PARENT_PATH/$v_out"

mkdir -pv "$GIT_FOLDER_PATH"
mkdir -pv "$ERROR_LOG_PATH"
mkdir -pv "$QUEUE_PATH"

# Check Tomcat version and directory
TOMCAT_7="tomcat7"
VAR_LOG_PATH="/var/log"
TOMCAT_PATH="/var/lib/$TOMCAT_7"
TOMCAT_WEB_PATH="$TOMCAT_PATH/webapps"
TOMCAT_LOG_PATH="$VAR_LOG_PATH/$TOMCAT_7"

checkGitdir(){
    if [ "$(ls -A $GIT_FOLDER_PATH 2>/dev/null)" ]
    then
        echo "Git folder exists... updating from repo"
        git -C $GIT_FOLDER_PATH pull origin master
        #cd $GIT_FOLDER_PATH
        #git pull origin master
    else
        echo "Cloning Applications from git...."
        git clone "$GITHUB_REPO_URL" "$GIT_FOLDER_PATH"
    fi
}

# Main Function to deploying peer
deployingPeer(){
    echo "*** SCHEDULER PEER $v_out DEPLOYMENT START ***"
    checkGitdir
    echo "*. Stop Tomcat server"
    service tomcat7 stop
    PROC_RESIDU=`ps ax |grep java |grep tomcat7 |awk '{print $1}'`
    if [ "$PROC_RESIDU" != '' ]
    then
        kill -9 $PROC_RESIDU
    fi
    echo "*. Create backup folder"
    mkdir -pv $BACKUP_PATH
    # Creating and copying folder for p2pserver utils
    mkdir -pv $P2PSERVER_PATH
    rsync -ah "$P2P_PUBLIC_FOLDER/" $P2PSERVER_PATH/ > /dev/null 2>&1
    # Check if bldb exist on backup folder. If exist, move with date
    if [ -d $BACKUP_PATH/bldb ]
    then
        mv -v $BACKUP_PATH/{bldb,bldb_"$(date +'%F@%T')"}
    fi
    # Checker for fresh installation or note
    if [ "$is_fresh" == 'TRUE' ]
    then
        # Clean tomcat logs
        rm $TOMCAT_LOG_PATH/*
        echo "*. Deploy new peer app"
        rm -rf "$TOMCAT_WEB_PATH/bldb" > /dev/null 2>&1
    else
        echo "*. Backup & clear tomcat log"
        mkdir -pv "$BACKUP_PATH/log_tomcat"
        if [ "$(ls -A $TOMCAT_LOG_PATH/)" ]
        then
            mv $TOMCAT_LOG_PATH/* $BACKUP_PATH/log_tomcat > /dev/null 2>&1
        fi
        echo "*. Backup old bldb...."
        if [ -d $TOMCAT_WEB_PATH/bldb ]
        then
            mv $TOMCAT_WEB_PATH/bldb $BACKUP_PATH && echo "bldb has been backup"
        fi
    fi
    # Unzip bldb into tomcat webapps
    unzip -qq "$SCHEDULER_RELEASE_PATH/bldb.zip" -d $TOMCAT_WEB_PATH
    echo "*. Copy properties file"
    cp -R $SCHEDULER_RELEASE_PATH"/properties/peer_unix/bldb" $TOMCAT_WEB_PATH
    echo "*. Set access permission"
    mkdir -pv /usr/share/tomcat7/common/classes
    mkdir -pv /usr/share/tomcat7/server/classes
    mkdir -pv /usr/share/tomcat7/shared/classes
    chmod -R 777 $TOMCAT_WEB_PATH"/bldb"
    echo "*. Start Tomcat server"
    service tomcat7 start
}

deployingPeer
if [ "$?" == '0' ]
then
    echo "*** DEPLOYMENT SUCCESS ! ***"
    # Removing github clone
    rm -rf $GIT_FOLDER_PATH
else
    echo "*** DEPLOYMENT FAILED ! ***"
    exit 2
fi
