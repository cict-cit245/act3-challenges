from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys

__authors__ = ["Member 1", "Member 2", "Member 3", "Member 4"]
__date__ = 20240925
__description__ = "Gather filesystem metadata of provided file and write it to a text file."

# Define the default output directory (using raw string to avoid issues with backslashes)
DEFAULT_OUTPUT_DIR = r"C:/Users/jaszline/Documents/act4-challenges/CHALLENGE_1/metadata_output"

# Ensure the output directory exists
if not os.path.exists(DEFAULT_OUTPUT_DIR):
    os.makedirs(DEFAULT_OUTPUT_DIR)

parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument("FILE_PATH", help="Path to file to gather metadata for")
parser.add_argument("-o", "--output", default="JuicyFairies.txt", help="Output text file for metadata")
args = parser.parse_args()

file_path = args.FILE_PATH
file_name = os.path.basename(file_path)  # Extract the filename from the path
output_file_name = args.output

# Create the full path for the output file by combining the output directory and the file name
output_file = os.path.join(DEFAULT_OUTPUT_DIR, output_file_name)

# Function to center text within a specific width
def center_text(text, width=80):
    return text.center(width)

# Gather metadata
stat_info = os.stat(file_path)
metadata = []

# Add title with the file name centered
metadata.append(center_text(f"Metadata of '{file_name}'"))  # Title header with file name
metadata.append("")  # Blank line for spacing

if "linux" in sys.platform or "darwin" in sys.platform:
    metadata.append(f"Creation time: {dt.fromtimestamp(stat_info.st_ctime)}")
elif "win" in sys.platform:
    metadata.append(f"Creation time: {dt.fromtimestamp(stat_info.st_ctime)}")
else:
    metadata.append(f"[-] Unsupported platform {sys.platform} detected. Cannot interpret creation/change timestamp.")

metadata.extend([
    "Modification time: " + str(dt.fromtimestamp(stat_info.st_mtime)),
    "Access time: " + str(dt.fromtimestamp(stat_info.st_atime)),
    "File mode: " + str(stat_info.st_mode),
    "File inode: " + str(stat_info.st_ino),
    "Device ID: " + str(stat_info.st_dev),
    "Number of hard links: " + str(stat_info.st_nlink),
    "Owner User ID: " + str(stat_info.st_uid),
    "Group ID: " + str(stat_info.st_gid),
    "File Size: " + str(stat_info.st_size),
    "Is a symlink: " + str(os.path.islink(file_path)),
    "Absolute Path: " + os.path.abspath(file_path),
    "File exists: " + str(os.path.exists(file_path)),
    "Parent directory: " + os.path.dirname(file_path),
    f"Parent directory: {os.path.dirname(file_path)} | File name: {os.path.basename(file_path)}"
])

# Add spacing between lines by appending empty lines
spaced_metadata = []
spaced_metadata.append(center_text(f"Metadata of '{file_name}'"))  # Ensure the title is centered
spaced_metadata.append("")  # Blank line after the title

# The rest of the content will be left-aligned, with blank lines for spacing
for line in metadata[2:]:  # Skip the title already added
    spaced_metadata.append(line)
    spaced_metadata.append("")  # Add blank line for spacing

# Print the title centered, and the rest left-aligned
for i, line in enumerate(spaced_metadata):
    if i == 0:  # Center the title only
        print(center_text(line))
    else:
        print(line)

# Write the metadata to the specified output file with the title centered and the rest left-aligned
with open(output_file, 'w') as f:
    for i, line in enumerate(spaced_metadata):
        if i == 0:  # Center the title in the output file
            f.write(center_text(line) + '\n')
        else:
            f.write(line + '\n')

print(f"Metadata written to {output_file}")

