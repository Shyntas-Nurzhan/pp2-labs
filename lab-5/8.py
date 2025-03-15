import re

def split_at_uppercase(s):
    return re.findall(r'[A-Z][^A-Z]*', s)

input_str = input()
print(split_at_uppercase(input_str))