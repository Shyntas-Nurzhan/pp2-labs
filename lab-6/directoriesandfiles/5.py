f = open("text.txt" , "a")

additional_info = ["apple" , "banana" , "cherry"]
for data in additional_info:
    f.write('\n' + data + '\n')

f = open("text.txt" , "r")
print(f.read())