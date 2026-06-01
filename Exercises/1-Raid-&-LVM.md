## Configuring Raid & creating LVM volumes
In this exercise you will get to try configuring Software RAID 5 on Linux and on top off this RAID 5 configuration you will create Logical volumes(LVM).

Do this exercise on a already installed virtual machine, add three new virtual disks 1Gbyte in size via the virtualmachine manager(VirtualBox, Hyper-V or whatever... )

Create one primary partition per disk and change the partition type to Linux Raid Autodetect (type fd).


Create the Raid 5 array by issuing the command:

```Bash
/sbin/mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1
``` 
This will take a while even if the command returns immidiately, if you used all of the disk size to your partitions it might take between 30 minutes to one hour.
But if you followed the instructions it won't take long... :-)

You can se the status of your newly created special device with the mdadm command:

```Bash
/sbin/mdadm --detail /dev/md0
```
```/dev/md0:
 Version : 0.90
 Creation Time : Mon Feb 16 14:51:11 2009
 Raid Level : raid5
 Array Size : 8401792 (8.01 GiB 8.60 GB)
 Used Dev Size : 4200896 (4.01 GiB 4.30 GB)
 Raid Devices : 3
 Total Devices : 3
Preferred Minor : 0
 Persistence : Superblock is persistent
 Update Time : Mon Feb 16 14:52:23 2009
 State : clean
 Active Devices : 3
Working Devices : 3
 Failed Devices : 0
 Spare Devices : 0
 Layout : left-symmetric
 Chunk Size : 64K
 UUID : f7285135:60b8e373:22efc361:f6df69d5 (local to host linux-raid)
 Events : 0.12
 Number Major Minor RaidDevice State
 0 8 17 0 active sync /dev/sdb1
 1 8 33 1 active sync /dev/sdc1
 2 8 49 2 active sync /dev/sdd1
```
The important lines to see are the **State** line which should say clean otherwise there might be a problem. At the bottom you should make sure that the **State** column always says active sync which says each device is actively in the array. You could potentially have a spare device that's on-hand should any drive should fail. If you have a spare you'll see it listed as such here.

One thing you'll see above if you're paying attention is the fact that the size of the array is 8G but I have three 4G drives as part of the array. That's because the extra space is used as extra parity data that is needed to survive the failure of one of the drives.

### Initial set of LVM on top of RAID
Now that we have /dev/md0 device you can create a Logical Volume on top of it. Why would you want to do that, except the fact that the LPIC level 2 exam will test tour knowledge on this topic? If I were to build an **ext3** filesystem on top of the RAID device and someday wanted to increase it's capacity I wouldn't be able to do that without backing up the data, building a new RAID array and restoring my data. Using **LVM** allows me to expand (or contract) the size of the filesystem without disturbing the existing data.

Anyway, here are the steps to then add this RAID array to the LVM system. The first command pvcreate will "initialize a disk or partition for use by LVM". The second command vgcreate will then create the Volume Group, in my case I called it lvm-raid:

```Bash
pvcreate /dev/md0

vgcreate lvm-raid /dev/md0 
```
If the `pvcreate` command failes, try writing zeros to the raid array with this command as root and the retry the pvcreate command:
```Bash
dd if=/dev/zero of=/dev/md0 bs=1M count=32
```
Ok, you've created a blank receptacle but now you have to tell how many Physical Extents from the physical device (`/dev/md0` in this case) will be allocated to this Volume Group. In my case I wanted all the data from `/dev/md0` to be allocated to this Volume Group. If later I wanted to add additional space I would create a new RAID array and add that physical device to this Volume Group.

To find out how many PEs are available to me use the vgdisplay command to find out how many are available and now I can create a Logical Volume using all (or some) of the space in the Volume Group. In my case I call the Logical Volume lvm0.

```Bash
vgdisplay lvm-raid 
```
```Bash
--- Volume group --- 
VG Name lvm-raid 
System ID Format lvm2 
Metadata Areas 1 Metadata Sequence No 1 
VG Access read/write 
VG Status resizable MAX LV 0 Cur
//Continued// 
LV 0 Open LV 0 Max PV 0 Cur PV 1 Act PV 1 VG Size 8.01 GB PE Size 4.00 MB Total PE 2051 Alloc PE / Size 0 / 0 Free PE / Size 2051 / 8.01 GB VG UUID skLMy3-3Uwf-cFll-01cp-BKKd-JJYy-caUpuf 
```
To create the logical volume called lvm0 issue the following command:
(Look that the PE number(2051) is the same that the Free PE / Size shows above)

```Bash
lvcreate -l 2051 lvm-raid -n lvm0 
```
In the end you will have a device you can use very much like a plain 'ol partition called /dev/lvm-raid/lvm0. You can now check on the status of the Logical Volume with the lvdisplay command. The device can then be used to to create a filesystem on.

```Bash
lvdisplay /dev/lvm-raid/lvm0 
```
```
--- Logical volume --- 
LV Name /dev/lvm-raid/lvm0 VG Name lvm-raid 
LV UUID xbR9q7-KpI6-COvJ-HdLL-nTeo-fy5x-wG0vFK 
LV Write Access read/write 
LV Status available #
//Continued// open 0 LV Size 8.01 GB Current LE 2051 Segments 1 Allocation inherit Read ahead sectors auto - currently set to 256 Block device 253:0 
 #mkfs.ext3 /dev/lvm-raid/lvm0 
```
Then mount the device to /mnt

```Bash
mount /dev/lvm-raid/lvm0 /mnt 
```
Check the available disk size with command:

```Bash
df -h /mnt 
```
```Bash
Filesystem Size Used Avail Use% Mounted on
/dev/mapper/lvm--raid-lvm0
 7.9G 147M 7.4G 2% /mnt
```
### Handling a Drive Failure
As everything eventually does break (some sooner than others) a drive in the array will fail. It is a very good idea to run `smartd` on all drives in your array (and probably ALL drives period) to be notified of a failure or a pending failure as soon as possible.
To simulate a hard drive error we will remove the SATA data cable from the hard drive on the top in the hard drive bay /dev/sdd.

You can also manually fail a partition, meaning to take it out of the RAID array, with the following command:
```Bash
/sbin/mdadm /dev/md0 -f /dev/sdd1 
mdadm: set /dev/sdd1 faulty in /dev/md0
```
Once the system has determined a drive has failed or is otherwise missing (you can disconnect the SATA cable from the harddrive on top in the bay to similate a drive failure or use the command above to manually fail a drive).
Iit will show something like this in mdadm:
```Bash
/sbin/mdadm --detail /dev/md0
/dev/md0:
 Version : 0.90
 Creation Time : Mon Feb 16 14:51:11 2009
 Raid Level : raid5
 Array Size : 8401792 (8.01 GiB 8.60 GB)
 Used Dev Size : 4200896 (4.01 GiB 4.30 GB)
 Raid Devices : 3
 Total Devices : 3
Preferred Minor : 0
 Persistence : Superblock is persistent
 Update Time : Mon Feb 16 15:37:21 2009
 State : clean, degraded
 Active Devices : 2
Working Devices : 2
 Failed Devices : 1
 Spare Devices : 0
 Layout : left-symmetric
 Chunk Size : 64K
 UUID : f7285135:60b8e373:22efc361:f6df69d5 (local to host linux-raid)
 Events : 0.14
 Number Major Minor RaidDevice State
 0 0 0 0 removed
 1 8 33 1 active sync /dev/sdb1
 2 8 49 2 active sync /dev/sdc1
 3 8 17 - faulty spare /dev/sdd1
```
You'll notice in this case I had /dev/sdd fail.

To test that the array still is functional copy or download something to the /mnt folder (if you do it as the raid user give him rights to the /mnt folder).

To simulate that we are going to replace the faulty harddrive, remove the harddrive from the array with the command:

```Bash
/sbin/mdadm /dev/md0 --remove /dev/sdd1
```
And the connect back the SATA data cable to the disk and issue the following command to rebuild the array:

```Bash
/sbin/mdadm /dev/md0 --add /dev/sdd1 
```
When you now check the status of your array you should see it rebuilding itself again, if you are quick enough issuing the command.

```Bash
/sbin/mdadm --detail /dev/md0
```
```Bash
/dev/md0:
 Version : 0.90
 Creation Time : Tue Feb 17 07:21:25 2009
 Raid Level : raid5
 Array Size : 8401792 (8.01 GiB 8.60 GB)
 Used Dev Size : 4200896 (4.01 GiB 4.30 GB)
 Raid Devices : 3
 Total Devices : 3
Preferred Minor : 0
 Persistence : Superblock is persistent
 Update Time : Tue Feb 17 10:14:01 2009
 State : clean, degraded, recovering
 Active Devices : 2
Working Devices : 3
 Failed Devices : 0
 Spare Devices : 1
 Layout : left-symmetric
 Chunk Size : 64K
 Rebuild Status : 28% complete
 UUID : 00342ed2:8fb9c8ec:22efc361:f6df69d5 (local to host linux-raid)
 Events : 0.1136
 Number Major Minor RaidDevice State
 0 8 17 0 active sync /dev/sdb1
 1 8 33 1 active sync /dev/sdc1
 3 8 49 2 spare rebuilding /dev/sdd1
```
Now try to delete or copy something to the /mnt folder, it should still be functional.

Take a screenshot showing the rebuild status and the files you have copied to the /mnt folder, upload the screenshot file here below.

You are finished with the exercise when you have uploaded the screenshot for your instructor to see.