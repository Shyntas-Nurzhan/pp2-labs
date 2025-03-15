import os

def is_exist(path):
    return os.access(path, os.F_OK)

path1 = r"C:\Users"

if (is_exist(path1) == True):
    print(f"The given path,named as {path1}, is exists")
    print(os.listdir(path1))
else:
    print("The given path doesn't exists")