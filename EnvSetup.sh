#!/bin/bash

# Variables
DB_USER="root"
DB_PASS="6666"
DB_NAME="dnfisreal"
BACKUP_FILE="dnfisreal_backup.sql"

# Install pymysql using pip
pip install pymysql

# Install MySQL server
apt-get -y install mysql-server

# Start MySQL service
service mysql start

# Change MySQL root user password and flush privileges
mysql -e "ALTER USER '$DB_USER'@'localhost' IDENTIFIED WITH mysql_native_password BY '$DB_PASS'; FLUSH PRIVILEGES;"

# Create a new database
mysql -u$DB_USER -p$DB_PASS -e "CREATE DATABASE $DB_NAME;"

# Use the new database and import data from the backup file
mysql -u$DB_USER -p$DB_PASS $DB_NAME < $BACKUP_FILE

# Install colab-xterm using pip
pip install colab-xterm

# Print a message indicating completion
echo "All tasks completed successfully."
