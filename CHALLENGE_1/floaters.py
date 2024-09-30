from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys

__authors__ = ["Dignomo", "Porado", "Sumalapao", "Wong"]
__date__ = "2024-09-25"
__description__ = "Gather filesystem metadata of provided file and store it in a well-formatted text file."

# Set up argument parsing
parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument("FILE_PATH", help="Path to file to gather metadata for")
args = parser.parse_args()
file_path = args.FILE_PATH

# Define a function to format the output neatly
def format_metadata(file_path):
    try:
        stat_info = os.stat(file_path)
        metadata = []

        # Add platform-specific creation/change time
        if "linux" in sys.platform or "darwin" in sys.platform:
            metadata.append(f"Creation/Change Time: {dt.fromtimestamp(stat_info.st_ctime)}")
        elif "win" in sys.platform:
            metadata.append(f"Creation Time: {dt.fromtimestamp(stat_info.st_ctime)}")
        else:
            metadata.append(f"[-] Unsupported platform {sys.platform} detected.")

        # Add other file attributes
        metadata.append(f"Modification Time: {dt.fromtimestamp(stat_info.st_mtime)}")
        metadata.append(f"Access Time: {dt.fromtimestamp(stat_info.st_atime)}")
        metadata.append(f"File Mode: {oct(stat_info.st_mode)}")
        metadata.append(f"File Inode: {stat_info.st_ino}")
        metadata.append(f"Device ID: {stat_info.st_dev}")
        metadata.append(f"Number of Hard Links: {stat_info.st_nlink}")
        metadata.append(f"Owner User ID: {stat_info.st_uid}")
        metadata.append(f"Group ID: {stat_info.st_gid}")
        metadata.append(f"File Size (bytes): {stat_info.st_size}")
        metadata.append(f"Is Symlink: {os.path.islink(file_path)}")
        metadata.append(f"Absolute Path: {os.path.abspath(file_path)}")
        metadata.append(f"File Exists: {os.path.exists(file_path)}")
        metadata.append(f"Parent Directory: {os.path.dirname(file_path)}")
        metadata.append(f"Parent Directory: {os.path.dirname(file_path)} | File Name: {os.path.basename(file_path)}")
        
        return "\n".join(metadata)
    
    except Exception as e:
        return f"Error gathering metadata: {e}"

# Gather metadata and format it
metadata_output = format_metadata(file_path)

# Create a folder named "metadata_output" in the same directory as the file
output_folder = os.path.join(os.path.dirname(file_path), "metadata_output")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Create the folder if it doesn't exist

# Prepare the output file path with the name "Floaters.txt"
output_file = os.path.join(output_folder, "Floaters.txt")

# Write metadata to the text file (overwrite mode, with UTF-8 encoding)
try:
    with open(output_file, "w", encoding="utf-8") as f:  # Specify UTF-8 encoding
        # Writing header and design elements
        f.write("\n" + "+" + "="*53 + "+\n")
        f.write("|         *** FILESYSTEM METADATA REPORT ***          |\n")
        f.write("+" + "="*53 + "+\n")
        f.write("\n")


        # Writing file-specific details
        f.write("   📄 File: {}\n".format(os.path.basename(file_path)))
        f.write("   ⏱  Generated On: {}\n".format(dt.now()))
        f.write("   📂 File Path: {}\n".format(file_path))
        f.write("\n" + "+" + "-"*53 + "+\n")
        
        # Adding metadata section headers
        f.write("|              +++ METADATA DETAILS +++               |\n")
        f.write("+" + "-"*53 + "+\n\n")

        # Grouping metadata for readability and vertical alignment
        f.write("➤ Timestamps:\n")
        f.write("   └─ Created:          {}\n".format(dt.fromtimestamp(os.stat(file_path).st_ctime)))
        f.write("   └─ Modified:         {}\n".format(dt.fromtimestamp(os.stat(file_path).st_mtime)))
        f.write("   └─ Accessed:         {}\n".format(dt.fromtimestamp(os.stat(file_path).st_atime)))

        f.write("\n➤ Permissions & Links:\n")
        f.write("   └─ File Mode:        {}\n".format(oct(os.stat(file_path).st_mode)))
        f.write("   └─ Number of Links:  {}\n".format(os.stat(file_path).st_nlink))

        f.write("\n➤ Ownership & Size:\n")
        f.write("   └─ Owner UID:        {}\n".format(os.stat(file_path).st_uid))
        f.write("   └─ Group GID:        {}\n".format(os.stat(file_path).st_gid))
        f.write("   └─ File Size:        {} bytes\n".format(os.stat(file_path).st_size))

        f.write("\n➤ File System Details:\n")
        f.write("   └─ Inode Number:     {}\n".format(os.stat(file_path).st_ino))
        f.write("   └─ Device ID:        {}\n".format(os.stat(file_path).st_dev))

        f.write("\n➤ Path & Existence:\n")
        f.write("   └─ Absolute Path:    {}\n".format(os.path.abspath(file_path)))
        f.write("   └─ Is Symlink:       {}\n".format(os.path.islink(file_path)))
        f.write("   └─ File Exists:      {}\n".format(os.path.exists(file_path)))
        f.write("   └─ Parent Directory: {}\n".format(os.path.dirname(file_path)))
        f.write("   └─ File Name:        {}\n".format(os.path.basename(file_path)))

        f.write("\n" + "+" + "-"*53 + "+\n")
        f.write("|               *** END OF REPORT ***                 |\n")
        f.write("+" + "="*53 + "+\n")

    # Notify the user and print the file location
    print(f"Metadata written to {output_file}")
    print(f"File saved in: {output_folder}")

except Exception as e:
    print(f"Error occurred while writing file: {e}")

# Also print metadata to console for quick reference
print("\nFile Metadata:")
print(metadata_output)
