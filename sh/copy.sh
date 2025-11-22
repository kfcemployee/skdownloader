#!/bin/bash

TARGET_DIR=${1:-"~/storage/downloads"}

cd "downloads/"
find -type f \( -name "*.mp3" -o -name "*.m4a" \) -exec cp {} "$TARGET_DIR" \;

cd ..
rm -rf downloads

echo "файлы скопированы в $TARGET_DIR"