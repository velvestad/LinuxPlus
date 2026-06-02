### Unused code
Code for this project that I wrote, but did not use.

```Bash
function du_in_percentage() {
    # Get the total disk space in bytes
    diskSpace=$(
        lsblk -d --bytes --output "SIZE" /dev/$1 | 
        grep "[0-9]"
        )

    # Calculate the total used space in bytes
    totalUsed=0
    for bytes in $(
        sed "s/[[:space:]]//" <(
        lsblk -f --bytes --output "FSAVAIL" /dev/$1 | 
        grep "[0-9]"
        )
    )
    do
        totalUsed=$(($totalUsed + $bytes))
    done

    # Return the percentage of used space
    echo "$(( $totalUsed * 100 / $diskSpace ))"
    return $(( $totalUsed * 100 / $diskSpace ))
}
```
```Bash
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
```
```Python
# Get todays lunch
def get_lunch(webresponse):
    lunch = webresponse.text[
        webresponse.text.index(" Dagens lunch i Övertorneå "):
    ].split("</strong>")[0].split("<strong>")[-1]
    return lunch
```
```Python
# Get todays date
def get_date(webresponse):
    date = webresponse.text[
    webresponse.text.index(" Dagens lunch i Övertorneå "):
    ].split("<br>")[0].split("<p>")[-1].split()

    return " ".join(date)
```