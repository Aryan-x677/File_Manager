import os
import shutil
import hashlib

# Define directories to store categorized files
categories = {
    'Documents': ['.txt', '.pdf', '.docx', '.xlsx', '.pptx'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Archives': ['.zip', '.tar', '.rar', '.gz'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Temp': ['.log', '.tmp', '.bak'],
}

def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()

def organize_files(source_dir):
    # Create category folders if they don't exist
    for category in categories:
        category_dir = os.path.join(source_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

    # Loop through files in the source directory and move them to the corresponding category
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        if os.path.isfile(file_path):
            file_ext = get_file_extension(filename)
            
            # Categorize the file based on extension
            for category, extensions in categories.items():
                if file_ext in extensions:
                    category_dir = os.path.join(source_dir, category)
                    destination = os.path.join(category_dir, filename)
                    shutil.move(file_path, destination)
                    print(f"Moved: {filename} to {category}")
                    break

def delete_temp_files(source_dir):
    # Delete temp files based on extensions
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            file_ext = get_file_extension(filename)
            if file_ext in categories['Temp']:
                os.remove(file_path)
                print(f"Deleted temp file: {filename}")

def remove_duplicates(source_dir):
    # Keep track of file hashes to identify duplicates
    seen_hashes = set()
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        if os.path.isfile(file_path):
            file_hash = hash_file(file_path)
            if file_hash in seen_hashes:
                os.remove(file_path)
                print(f"Deleted duplicate file: {filename}")
            else:
                seen_hashes.add(file_hash)

def hash_file(file_path):
    """Generate a hash for a file (SHA256 or MD5)."""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    source_directory = input("Enter the path to the directory to declutter: ")

    if os.path.exists(source_directory):
        organize_files(source_directory)
        delete_temp_files(source_directory)
        remove_duplicates(source_directory)
        print("Decluttering process complete!")
    else:
        print("Directory does not exist.")
