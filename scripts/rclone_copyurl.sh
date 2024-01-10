#!/bin/bash

if [ -z "$1" ]; then
  echo "Vui lòng cung cấp tên tệp chứa danh sách URL"
  exit 1
fi

if [ -z "$2" ]; then
  echo "Vui lòng cung cấp tên tệp"
  exit 1
fi

nohup ~/_rclone_copyurl.sh $1 $2 > ~/real-debrid.log 2>&1 &
