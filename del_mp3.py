import os
import glob

# Define the root directory
root_directory = './export/audio/'

# Find all .mp3 files in the root directory and its subdirectories
mp3_files = glob.glob(root_directory + '**/*.mp3', recursive=True)

# Iterate over the list of .mp3 files and remove each one
for mp3_file in mp3_files:
    try:
        os.remove(mp3_file)
        print(f"Removed: {mp3_file}")
    except Exception as e:
        print(f"Error removing {mp3_file}: {e}")

print("All .mp3 files have been removed.")
