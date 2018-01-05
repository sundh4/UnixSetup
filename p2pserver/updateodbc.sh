#!/bin/sh

echo "Backup Current /etc/odbc.ini -> /etc/odbc.ini.old"
yes | /bin/cp /etc/odbc.ini /etc/odbc.ini.old

echo "Copying New /mnt/public/IT/DSN/unix/odbc.ini -> /etc/odbc.ini"
yes | /bin/cp /mnt/public/IT/DSN/unix/odbc.ini /etc/odbc.ini
