#!/bin/bash

if [ -z "$1" ]; then
  echo "Vui lòng cung cấp tên tệp"
  exit 1
fi

nohup rclone copy real-debrid:links "trois:$1" --filter-from ~/filter-real-debrid.txt  --transfers 2 --checkers 2 --multi-thread-streams 2  --multi-thread-cutoff 100M --onedrive-chunk-size 100M --bwlimit 0 --fast-list -v --retries 5 > ~/real-debrid.log 2>&1 &
