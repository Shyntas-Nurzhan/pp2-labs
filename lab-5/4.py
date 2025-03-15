import re

def seq(string):
    pattern = r'^[A-Z]{1}[a-z]+$'
    return bool(re.match(pattern , string))

txt = input()
x = seq(txt)

print(x)