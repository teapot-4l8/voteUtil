#!/bin/bash

# Variables
DB_USER="root"
DB_PASS="6666"
DB_NAME="dnfisreal"

# Execute MySQL command
mysql -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "UPDATE user_data SET remain_votes = 50;"

echo "MySQL command executed successfully!"
