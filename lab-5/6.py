import re 

pattern = r'[ ,.]' 

txt = input("Enter text: ")

x = re.sub(pattern, ":", txt)

print(x)