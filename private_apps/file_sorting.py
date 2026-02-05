import os
import shutil
import hashlib
from datetime import datetime

# Base directory
BASE_DIR = "/media/uch"
DEST_DIR = os.path.join(BASE_DIR, "sorted_folder_by_python")

# Destination subfolders
IMG_DIR = os.path.join(DEST_DIR, "images")
VID_DIR = os.path.join(DEST_DIR, "videos")
PDF_DIR = os.path.join(DEST_DIR, "pdfs")
TXT_DIR = os.path.join(DEST_DIR, "texts")
DOC_DIR = os.path.join(DEST_DIR, "docs")     # zip files
DUP_DIR = os.path.join(DEST_DIR, "duplicates")

# Log file path
LOG_FILE = os.path.join(DEST_DIR, "sort_log.txt")

# File extension categories
IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', 'heic', 'arw'}
VIDEO_EXT = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', 'thm'}
PDF_EXT = {'.pdf'}
TXT_EXT = {'.txt'}
DOC_EXT = {'.zip', '.docx', '.xlsx', '.csv', '.doc', '.asc'}

# Create directories
for directory in [IMG_DIR, VID_DIR, PDF_DIR, TXT_DIR, DOC_DIR, DUP_DIR]:
    os.makedirs(directory, exist_ok=True)

# Initialize log
def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def resolve_name_conflict(dest_folder, filename):
    """Resolve duplicate filename by adding timestamp"""
    dest_file = os.path.join(dest_folder, filename)
    if not os.path.exists(dest_file):
        return dest_file
    name, ext = os.path.splitext(filename)
    new_name = f"{name}_{int(os.path.getmtime(dest_file))}{ext}"
    return os.path.join(dest_folder, new_name)

def get_destination(file):
    """Determine destination folder based on extension"""
    ext = os.path.splitext(file)[1].lower()
    if ext in IMAGE_EXT:
        return IMG_DIR
    elif ext in VIDEO_EXT:
        return VID_DIR
    elif ext in PDF_EXT:
        return PDF_DIR
    elif ext in TXT_EXT:
        return TXT_DIR
    elif ext in DOC_EXT:
        return DOC_DIR
    else:
        return None  # Unknown file type

# Traverse and process files
for root, dirs, files in os.walk(BASE_DIR):
    # Skip the destination folder itself
    if DEST_DIR in root:
        continue

    for filename in files:
        src_file = os.path.join(root, filename)

        if not os.path.isfile(src_file):
            continue

        dest_folder = get_destination(src_file)

        if dest_folder:
            dest_file = os.path.join(dest_folder, filename)

            if os.path.exists(dest_file):
                if get_file_hash(src_file) == get_file_hash(dest_file):
                    # Duplicate
                    dup_dest = resolve_name_conflict(DUP_DIR, filename)
                    shutil.move(src_file, dup_dest)
                    log(f"DUPLICATE: {src_file} -> {dup_dest}")
                    continue
                else:
                    # Rename to avoid conflict
                    dest_file = resolve_name_conflict(dest_folder, filename)

            shutil.copy2(src_file, dest_file)
            log(f"COPY: {src_file} -> {dest_file}")
        else:
            # Delete unknown file
            try:
                os.remove(src_file)
                log(f"DELETE: {src_file}")
            except Exception as e:
                log(f"ERROR deleting {src_file}: {e}")
