import os, platform

print(f"Hello, {os.getlogin()}!")
print(f"You're running Python {platform.python_version()} on {platform.system()}.")
print(f"Current directory: {os.getcwd()}")