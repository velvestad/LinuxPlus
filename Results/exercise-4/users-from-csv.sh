#!/bin/bash
csv_file="$1"

lc=$( sed "s/[^0-9]//g" <(wc --lines "$csv_file") )

echo "Username:Password" > username.password

for ((i=1; i<=lc; i++))
do
    user=( $( sed -n "${i}p" "$csv_file" | tr -d '\r' ) )
    
    IFS=',' read -r username group <<< "$user"
    password=$(echo -e "$(tr -dc 'A-Za-z0-9!@#$%^&*()' < /dev/urandom | head -c 12)\n")

    useradd $username
    echo "$username:$password" | chpasswd
    groupadd $group
done
