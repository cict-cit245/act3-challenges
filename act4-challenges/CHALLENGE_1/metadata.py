from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys

__authors__ = ["Member 1", "Member 2", "Member 3", "Member 4"]
__date__ = 20240925
__description__ = "Gather filesystem metadata of provided file and write it to a text file."

# Define the default output directory (using raw string to avoid issues with backslashes)
DEFAULT_OUTPUT_DIR = r"C:\Users\jaszline\Desktop\Cyberforensics\act4-challenges\CHALLENGE_1\metadataoutput"

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
output_file_name = args.output

# Create the full path for the output file by combining the output directory and the file name
output_file = os.path.join(DEFAULT_OUTPUT_DIR, output_file_name)

# Gather metadata
stat_info = os.stat(file_path)
metadata = []

if "linux" in sys.platform or "darwin" in sys.platform:
    metadata.append(f"Change time: {dt.fromtimestamp(stat_info.st_ctime)}")
elif "win" in sys.platform:
    metadata.append(f"Creation time: {dt.fromtimestamp(stat_info.st_ctime)}")
else:
    metadata.append(f"[-] Unsupported platform {sys.platform} detected. Cannot interpret creation/change timestamp.")

metadata.extend([
    f"Modification time: {dt.fromtimestamp(stat_info.st_mtime)}",
    f"Access time: {dt.fromtimestamp(stat_info.st_atime)}",
    f"File mode: {stat_info.st_mode}",
    f"File inode: {stat_info.st_ino}",
    f"Device ID: {stat_info.st_dev}",
    f"Number of hard links: {stat_info.st_nlink}",
    f"Owner User ID: {stat_info.st_uid}",
    f"Group ID: {stat_info.st_gid}",
    f"File Size: {stat_info.st_size}",
    f"Is a symlink: {os.path.islink(file_path)}",
    f"Absolute Path: {os.path.abspath(file_path)}",
    f"File exists: {os.path.exists(file_path)}",
    f"Parent directory: {os.path.dirname(file_path)}",
    f"Parent directory: {os.path.dirname(file_path)} | File name: {os.path.basename(file_path)}"
])

# Print to console
for line in metadata:
    print(line)

# Write to the specified output file in the desired directory
with open(output_file, 'w') as f:
    for line in metadata:
        f.write(line + '\n')

print(f"Metadata written to {output_file}")
