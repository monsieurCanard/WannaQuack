#!/bin/bash

FILE_EXTENSIONS=("ots" "docx" "xlsx" "pptx" "pdf" "txt" "jpg" "png" "mp4" "mp3")


TARGET_DIR="/home/infection"

if [ ! -d "$TARGET_DIR" ]; then
	mkdir -p "$TARGET_DIR"
	chmod 777 "$TARGET_DIR"
fi


for i in {1..5}; do
	mkdir -p "$TARGET_DIR/dir$i"
	for j in {1..5}; do
		FILE="$TARGET_DIR/dir$i/files_$j.${FILE_EXTENSIONS[$((j % ${#FILE_EXTENSIONS[@]}))]}"
		chmod 777 "$TARGET_DIR/dir$i"
		touch "$FILE"
		chmod 777 "$FILE"
		echo "Ceci est de la data, enjoy !" > "$FILE" 
	done

done
