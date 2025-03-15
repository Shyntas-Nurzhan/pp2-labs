import os

def copy_file(source, destination):
    if not os.path.exists(source):
        print("Source file does not exist.")
        return

    with open(source, 'r') as src, open(destination, 'w') as dest:
        dest.write(src.read())

    print(f"Contents copied from {source} to {destination}")

copy_file("source.txt", "destination.txt")