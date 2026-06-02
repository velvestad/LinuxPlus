#!/bin/bash

# Function declarations
function get_disks {
    # Create an array with the disks on the system
    declare -a disks
    for disk in $(
        lsblk --list --output "NAME,SIZE,TYPE" | 
        grep disk | 
        awk '{print $1}'
    )
    do 
        disks+=($disk)
    done
    echo "${disks[@]}"
}

# Create an array with the disks on the system
declare -a disks=($(get_disks))

# Find total size of all disks
total_size=0
for disk in "${disks[@]}"
do
    disk_size=$(
        lsblk -d --bytes --output "SIZE" /dev/$disk | 
        grep [0-9]
    )
    total_size=$((total_size + disk_size))
done


# Find total space on filesystems
total_used_fs=0
for bytes in $(
    sed "s/[[:space:]]//" <(
        lsblk -fs --bytes --output "SIZE,MOUNTPOINTS" | grep /
        )
    )
do  
    val=$(echo $bytes | tr -cd '0-9')
    if [ "$val" ]; then 
        total_used_fs=$((total_used_fs + val))
    fi
done


# Find total available space on filesystems
total_avail=0
for bytes in $(
    sed "s/[[:space:]]//" <(
        lsblk -fs --bytes --output "FSAVAIL" | 
        grep [0-9]
        )
    )
do
    total_avail=$((total_avail + bytes))
done


# Calculate disk usage in percentage
total_du=$((total_used_fs - total_avail))
percentage=$(
    echo "scale=2; 
    $total_du * 100 / $total_size" | 
    bc
    )

echo -e "Total hard drive usage: $percentage%\n" > ./diskusage.txt

# List partitions and their sizes
echo "Partitions and their sizes:" >> ./diskusage.txt
sed "s/[[:space:]]\+\S\+$//" <(
    lsblk -s --output "NAME,SIZE,TYPE" | egrep "part|lvm"
) >> ./diskusage.txt


# List disk usage of directories in /home
echo -e "\nDisk usage of directories in /home:" >> ./diskusage.txt
du -h --max-depth=0 /home/* >> ./diskusage.txt
