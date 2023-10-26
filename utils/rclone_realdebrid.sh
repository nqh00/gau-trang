#!/bin/bash

if [ -z "$1" ]; then
  echo "Vui lòng cung cấp tên tệp"
  exit 1
fi

nohup rclone copy real-debrid:links "onedrive:$1" --filter-from ~/filter-real-debrid.txt  --transfers 10 --checkers 20 --bwlimit 0 --onedrive-chunk-size 20M --fast-list -v --retries 5 > ~/real-debrid.log 2>&1 &
