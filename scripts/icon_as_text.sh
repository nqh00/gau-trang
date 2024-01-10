#!/bin/bash

# sudo apt install imagemagick
if [ -z "$1" ]; then
  echo "Vui lòng cung cấp tên tệp"
  exit 1
fi

convert -size 256x256 xc:none -fill '#FFA100' -font Archivo-Bold.ttf -pointsize 100 -gravity South -annotate +0+25% $1 /var/www/webdav/icons/$1.png
