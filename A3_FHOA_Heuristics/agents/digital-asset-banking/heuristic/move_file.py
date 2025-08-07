import shutil
import os

def move_file(source_path: str, destination_path: str):
    """
    Moves a file from a source path to a destination path.

    The destination can be a folder, and the file will be moved inside it
    with the same name. Or, the destination can be a full path including
    a new filename.

    Args:
        source_path (str): The full path to the file to be moved.
        destination_path (str): The full path to the destination folder or file.
    """
    try:
        # shutil.move is powerful; it can move files across different drives.
        shutil.move(source_path, destination_path)
        print(f"✅ Successfully moved '{source_path}' to '{destination_path}'")
    except FileNotFoundError:
        print(f"❌ Error: The source file '{source_path}' was not found.")
    except shutil.Error as e:
        # This can happen if the destination file already exists.
        print(f"❌ Error moving file: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == '__main__':
    # --- IMPORTANT ---
    # Replace these placeholder paths with the actual source file and destination.
    source = "replace_with_source_path/file.txt"
    destination = "replace_with_destination_folder/"

    if "replace_with" in source:
        print("👉 Please edit this script and replace the placeholder paths before running.")
    else:
        move_file(source, destination)