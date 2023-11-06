#!/bin/bash

#nohup cat < $1 | xargs -P 10 -I {} sh -c 'url=$(echo "{}" | cut -f1); folder_name=$(echo "{}" | cut -f2); rclone copyurl "$url" "onedrive:$folder_name" -a -v --no-clobber' -- {} > ~/log 2>&1 &
while IFS= read -r url; do
    rclone copyurl "$url" "onedrive:$2" -a -v --no-clobber
done < $1
