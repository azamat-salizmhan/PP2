import shutil
import os

# create directory
os.makedirs("storage", exist_ok=True)

# move file
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "storage/sample.txt")
    print("File moved to storage folder")

# copy file
shutil.copy("storage/sample.txt", "storage/sample_copy.txt")
print("File copied inside storage")
