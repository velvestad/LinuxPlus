#### What is done:
- Initialized disks with label ann partitions.
- Created array `/dev/md0`
- Created logical volume `lvm0`
- Created xfs filesyestem on `lv0m`
- Simulated drive failure on `sdd1` with command `/mnt$ sudo /sbin/mdadm /dev/md0 -f /dev/sdd1`
- Removed and added the disk back to the array.
- Screenshot of rebuilding process uploaded on Moodle.