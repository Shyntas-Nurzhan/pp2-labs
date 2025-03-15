import re

def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

input_str = input()
print(camel_to_snake(input_str))