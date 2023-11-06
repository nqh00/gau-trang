#!/bin/bash

DESTINATION_PATH="onedrive:"
LOCAL_PATH=".temp"
SOURCE_PATH="real-debrid:links"

copied_files=0

rclone ls "$SOURCE_PATH" | while read -r line; do
    file=$(echo "$line" | awk '{$1=""; print $0}' | sed 's/^[ \t]*//;s/[ \t]*$//')

    if rclone ls "$DESTINATION_PATH/$file" >/dev/null 2>&1; then
        echo "Tệp $file đã tồn tại trên đích. Không cần tải và sao chép lại."
    else
        rclone copy "$SOURCE_PATH/" "$LOCAL_PATH/" --include="$file" --ignore-size

        if [ $? -eq 0 ]; then
            echo "Tải tệp $file thành công từ nguồn đến máy local."

            rclone copy "$LOCAL_PATH/" "$DESTINATION_PATH/" --include="$file" --ignore-size -v

            if [ $? -eq 0 ]; then
                echo "Sao chép tệp $file từ máy local đến đích thành công."
                rm -f "$LOCAL_PATH/$file"
                echo "Xóa tệp $file khỏi máy local thành công."
                ((copied_files++))
            else
                echo "Lỗi khi sao chép tệp $file từ máy local đến đích."
                exit 1
            fi
        else
            echo "Lỗi khi tải tệp $file từ nguồn đến máy local."
            exit 1
        fi
    fi
done

echo "Đã sao chép $copied_files tệp vào đích."
