import os
import shutil

def move_files_to_parent(filenames: list[str]):
    """
    Iterates through a list of filenames and moves each file from the
    current directory to the parent directory.

    Args:
        filenames (list[str]): A list of file names to move.
    """
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    print(f"Current directory: {current_dir}")
    print(f"Destination (parent) directory: {parent_dir}\n")

    if not filenames:
        print("No files specified to move.")
        return

    for filename in filenames:
        source_path = os.path.join(current_dir, filename)
        # The destination for shutil.move can be the directory itself.
        destination_path = parent_dir

        try:
            if not os.path.exists(source_path):
                print(f"⚠️  Skipping '{filename}': Source file not found at '{source_path}'")
                continue

            print(f"Attempting to move '{filename}' to '{parent_dir}'...")
            shutil.move(source_path, destination_path)
            print(f"✅ Successfully moved '{filename}'")

        except shutil.Error as e:
            # This can happen if the destination file already exists.
            print(f"❌ Error moving '{filename}': {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred while moving '{filename}': {e}")
        print("-" * 20)


if __name__ == '__main__':
    # --- IMPORTANT ---
    # Add the names of the files you want to move into this list.
    # For this to work, you must first create these files in the same
    # directory as this script.
    files_to_move = [
        "file1.txt",
        "data.csv",
        "archive.zip",
    ]

    print("--- Starting file move process ---")
    move_files_to_parent(files_to_move)
    print("\n--- Process finished ---")