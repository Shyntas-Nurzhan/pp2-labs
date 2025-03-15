import os

def list_directories(path):
    directories = []
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            directories.append(dir)
    return directories

def list_files(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files

def list_all(path):
    return os.listdir(path)

path = "C:\Program Files\Android\jdk\jdk-8.0.302.8-hotspot\jdk8u302-b08\jre"

print(list_directories(path))
print(list_files(path))
print(list_all(path))