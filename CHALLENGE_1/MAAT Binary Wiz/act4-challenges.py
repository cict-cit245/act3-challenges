from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys

__authors__ = ["Carl James Tito", "Rhowena Alimeos", "John Marty Arendain", "Ailen Grace Malcon"]
__date__ = "2024-09-25"
__description__ = "Gather filesystem metadata of provided file"

# Argument parser setup
parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument("FILE_PATH", help="Path to the file to gather metadata for")
args = parser.parse_args()
file_path = args.FILE_PATH

# Check if file exists
if not os.path.exists(file_path):
    print("[-] Error: File '{}' does not exist.".format(file_path))
    sys.exit(1)

# Create the "MAAT Binary Wiz_METADATA_OUPUTS" directory if it doesn't exist
output_dir = "MAAT Binary Wiz_METADATA_OUPUTS"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate a unique filename based on the file's name, but output will be .txt
file_name, _ = os.path.splitext(os.path.basename(file_path))  # Ignore the original extension
output_file = os.path.join(output_dir, f"metadata_{file_name}.txt")  # Output always ends with .txt

# Helper function to format and center data in table columns
def format_row(left, right, width=50):
    return "| " + left.center(width) + " | " + right.center(width) + " |\n"

try:
    # Gather file stats
    stat_info = os.stat(file_path)

    with open(output_file, "w") as f:
        # Write the header
        f.write("+" + "-"*104 + "+\n")
        f.write("|" + " MAAT Binary Wiz Metadata ".center(104) + "|\n")
        f.write("+" + "-"*104 + "+\n\n")

        # Write file information in table form
        f.write(format_row("Attribute", "Value"))
        f.write("+" + "-"*104 + "+\n")
        f.write(format_row("File Name", os.path.basename(file_path)))
        f.write(format_row("File Path", file_path))
        f.write(format_row("File Size", "{} bytes".format(stat_info.st_size)))
        f.write(format_row("File Type", "Directory" if os.path.isdir(file_path) else "File"))
        f.write("+" + "-"*104 + "+\n")

        # Write timestamp information
        f.write(format_row("Creation Time", dt.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S")))
        f.write(format_row("Modification Time", dt.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S")))
        f.write(format_row("Access Time", dt.fromtimestamp(stat_info.st_atime).strftime("%Y-%m-%d %H:%M:%S")))
        f.write("+" + "-"*104 + "+\n")

        # Write permission information
        f.write(format_row("File Mode (Octal)", oct(stat_info.st_mode)))
        f.write(format_row("Readable", "Yes" if stat_info.st_mode & 0o400 else "No"))
        f.write(format_row("Writable", "Yes" if stat_info.st_mode & 0o200 else "No"))
        f.write(format_row("Executable", "Yes" if stat_info.st_mode & 0o100 else "No"))
        f.write("+" + "-"*104 + "+\n")

        # Write ownership information
        f.write(format_row("Owner User ID (UID)", str(stat_info.st_uid)))
        f.write(format_row("Group ID (GID)", str(stat_info.st_gid)))
        f.write("+" + "-"*104 + "+\n")

        # Write other metadata
        f.write(format_row("Inode", str(stat_info.st_ino)))
        f.write(format_row("Device ID", str(stat_info.st_dev)))
        f.write(format_row("Number of Hard Links", str(stat_info.st_nlink)))
        f.write("+" + "-"*104 + "+\n\n")

        # Write footer
        f.write("+" + "-"*104 + "+\n")
        f.write("|" + " End of Metadata ".center(104) + "|\n")
        f.write("+" + "-"*104 + "+\n")

    print("[+] Metadata written to '{}'".format(output_file))

except Exception as e:
    print(f"[-] Error: {e}")
    sys.exit(1)
