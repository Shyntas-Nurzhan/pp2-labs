import re

def matching(string):
    pattern = r'^ab*$'
    return bool(re.match(pattern, string))

test = input()
x = matching(test)
print(x)