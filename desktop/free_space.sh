#!/bin/bash

# Get free space information for /dev/nvme0n1p4
free_space=$(df -h /dev/nvme0n1p4 | awk 'NR==2 {print $4}')
used_percent=$(df -h /dev/nvme0n1p4 | awk 'NR==2 {print $5}')
total_size=$(df -h /dev/nvme0n1p4 | awk 'NR==2 {print $2}')
used_space=$(df -h /dev/nvme0n1p4 | awk 'NR==2 {print $3}')

# Create notification message
message="Main Drive (/dev/nvme0n1p4)
Total: $total_size
Used: $used_space ($used_percent) | Free: $free_space"

# Send notification
notify-send -t 8000 -u normal "Disk Space Status" "$message"
