import re

def split_at_uppercase(s):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)

input_str = input()
print(split_at_uppercase(input_str))