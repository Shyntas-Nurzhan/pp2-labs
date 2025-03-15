import os

path = "C:\Program Files\Android\jdk\jdk-8.0.302.8-hotspot\jdk8u302-b08\LICENSE"

print("Specific path exists: " , os.access(path, os.F_OK))
print("Specific file is readable: " , os.access(path, os.R_OK))
print("Specific file is changable: " , os.access(path, os.W_OK))
print("Specific file is executable: " , os.access(path, os.X_OK))