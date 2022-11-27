#!/bin/bash


# Read environment variables from .env file
export $(grep -v '^#' ../.env | xargs)


# Output text colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color


if [ "$1" = "start" ]
    then 
        sudo systemctl start mysql
        echo "MySQL server is currently ${GREEN}ACTIVE${NC}"

elif [ "$1" = "stop" ]
    then 
        sudo systemctl stop mysql
        echo "MySQL server is currently ${RED}INACTIVE${NC}"

elif [ "$1" = "status" ]
    then
        sudo service mysql status

elif [ "$1" = "reset" ]
    then
        sudo systemctl start mysql
        mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$database" --execute="DROP DATABASE ${2-$MYSQL_DATABASE};" > /dev/null 2>&1
        mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" --database="$database" --execute="CREATE DATABASE ${2-$MYSQL_DATABASE};" > /dev/null 2>&1
        echo "'${2-$MYSQL_DATABASE}' database has been reset. MySQL server is currently ${GREEN}ACTIVE${NC}"

else
    echo "
    ${YELLOW}Incorrect or no argument supplied. Please choose from the following:${NC}
    - start: to start the mysql server
    - stop: to stop the mysql
    - status: check current status of the MySQL server
    - reset <database_name>: Deletes (if possible) and creates the selected database; if no database_name argument is given, reset the '$MYSQL_DATABASE' database (from .env)
    "
fi
