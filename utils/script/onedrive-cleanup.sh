#!/bin/bash

if [ -z "$1" ]; then
  echo "Vui lòng cung cấp tên remote cho rclone"
  exit 1
fi

REMOTE="$1"

rclone about "${REMOTE}:"
ACCESS_TOKEN="$(rclone config dump | jq -r --arg remote "$REMOTE" '.[$remote].token | fromjson | .access_token')"
DRIVE_ID="$(rclone config dump | jq -r --arg remote "$REMOTE" '.[$remote].drive_id')"

function get_dir {
    ITEM_ID="$1"

    echo "Listing directory: ${ITEM_ID}"
    curl -s \
      -X 'GET' \
      -H "Authorization: Bearer ${ACCESS_TOKEN}" \
      -H 'Accept: application/json' \
      "https://graph.microsoft.com/v1.0/drives/${DRIVE_ID}/items/${ITEM_ID}/children" \
      | jq -r '.value[] | "\(if (.file != null) then "file" else "directory" end) \(.id)"' \
      | while read -r TYPE ID; do
            if [[ "$TYPE" == "file" ]]; then
                get_versions "$ID"
            else
                get_dir "$ID"
            fi
        done
}

function get_versions {
    ITEM_ID="$1"

    echo "Checking versions for: ${ITEM_ID}"
    curl -s \
      -X 'GET' \
      -H "Authorization: Bearer ${ACCESS_TOKEN}" \
      -H 'Accept: application/json' \
      "https://graph.microsoft.com/v1.0/drives/${DRIVE_ID}/items/${ITEM_ID}/versions" \
    | jq -r '.value[].id' \
    | tail -n+2 \
    | while read -r VERSION_ID; do
          echo "Removing version: ${VERSION_ID}"

          curl -s \
            -X 'DELETE' \
            -H "Authorization: Bearer ${ACCESS_TOKEN}" \
            -H 'Accept: application/json' \
            "https://graph.microsoft.com/v1.0/drives/${DRIVE_ID}/items/${ITEM_ID}/versions/${VERSION_ID}"
      done
}

get_dir root
