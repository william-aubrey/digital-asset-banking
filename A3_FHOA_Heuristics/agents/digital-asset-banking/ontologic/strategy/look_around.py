import os

def list_items(path="."):
    """Lists files and directories in a given path."""
    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        print(f"Error: Directory '{path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_items()
