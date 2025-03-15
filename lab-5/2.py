import re

def matching(string):
    pattern = r'^ab{2,3}$'
    return bool(re.match(pattern, string))

test = input()
x = matching(test)
print(x)