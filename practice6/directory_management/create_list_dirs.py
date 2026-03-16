import os

# create directories
os.makedirs("test_dir/sub_dir", exist_ok=True)
print("Directories created.")

# list files and folders
print("Current directory files:")
print(os.listdir())

# show current working directory
print("Current path:", os.getcwd())
