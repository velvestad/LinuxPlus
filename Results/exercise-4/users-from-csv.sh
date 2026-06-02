#!/bin/bash
csv_file="$1"

# Count lines in csv file to know how many users to create
lc=$( sed "s/[^0-9]//g" <(wc --lines "$csv_file") )

echo "Username:Password" > username.password

for ((n=1; n<=lc; n++))
do
    # Parse line n in csv file
    user=( $( sed -n "${n}p" "$csv_file" | tr -d '\r' ) )
    
    # Parse username and group from the line
    IFS=',' read -r username group <<< "$user"

    # Generate a random 12 character password
    password=$(echo -e "$(tr -dc 'A-Za-z0-9!@#$%^&*()' < /dev/urandom | head -c 12)\n")

    # Creates the user, group and set the password
    useradd $username
    groupadd $group 2> /dev/null
    echo "$username:$password" | chpasswd

    # Add the username and password to the file
    echo "$username:$password" >> username.password
done
