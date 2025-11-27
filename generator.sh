#!/bin/bash

TARGET_DIR="/home/infection"

if [ ! -d "$TARGET_DIR" ]; then
	mkdir -p "$TARGET_DIR"
fi


for i in {1..5}; do
	mkdir -p "$TARGET_DIR/dir$i"
	for j in {1..5}; do
		FILE="$TARGET_DIR/dir$i/files_$j" 
		touch "$FILE"
		chmod 777 "$FILE"
		echo "Ceci est de la data, enjoy !" > "$FILE" 
	done

done
