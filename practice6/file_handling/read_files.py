# read_files.py

with open("sample.txt", "r") as file:
    print("Using read():")
    print(file.read())

with open("sample.txt", "r") as file:
    print("Using readline():")
    print(file.readline())

with open("sample.txt", "r") as file:
    print("Using readlines():")
    lines = file.readlines()
    print(lines)
