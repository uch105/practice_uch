#!/bin/bash

# Mount point of your HDD (adjust if needed)
BASE_DIR="/media/uch"
DEST_DIR="$BASE_DIR/sorted_folder_by_bash"

# Destination subfolders
IMG_DIR="$DEST_DIR/images"
VID_DIR="$DEST_DIR/videos"
OTH_DIR="$DEST_DIR/files"

# Create destination folders
mkdir -p "$IMG_DIR" "$VID_DIR" "$OTH_DIR"

# Function to compute file hash
file_hash() {
    sha256sum "$1" | awk '{print $1}'
}

# Loop through all files excluding the sorted_folder_by_bash directory
find "$BASE_DIR" -type f ! -path "$DEST_DIR/*" | while read -r file; do
    # Get lowercase extension
    ext="${file##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    # Decide destination folder
    case "$ext_lower" in
        jpg|jpeg|png|gif|bmp|webp|tiff)
            target_dir="$IMG_DIR"
            ;;
        mp4|mkv|avi|mov|flv|wmv|webm)
            target_dir="$VID_DIR"
            ;;
        *)
            target_dir="$OTH_DIR"
            ;;
    esac

    # Get base filename only
    filename=$(basename "$file")

    # Check if file already exists in destination
    dest_file="$target_dir/$filename"
    if [[ -f "$dest_file" ]]; then
        # Compare hash of both files
        if [[ "$(file_hash "$file")" == "$(file_hash "$dest_file")" ]]; then
            echo "Skipping duplicate: $filename"
            continue
        else
            # Rename to avoid conflict
            base="${filename%.*}"
            ext="${filename##*.}"
            timestamp=$(date +%s)
            dest_file="$target_dir/${base}_$timestamp.$ext"
        fi
    fi

    # Copy file
    cp "$file" "$dest_file"
    echo "Copied: $file -> $dest_file"
done
