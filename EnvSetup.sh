#!/bin/bash

# Install pymysql using pip
pip install pymysql

# Install MySQL server
apt-get -y install mysql-server

# Start MySQL service
service mysql start

# Change MySQL root user password and flush privileges
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '6666'; FLUSH PRIVILEGES;"

# Install colab-xterm using pip
pip install colab-xterm

# Print a message indicating completion
echo "All tasks completed successfully."