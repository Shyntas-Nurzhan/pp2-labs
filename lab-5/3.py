import re

def seq(string):
    pattern = r'^[a-z]{1}(_[a-z])+$'
    return bool(re.match(pattern, string))

txt = input()
x = seq(txt)
print(x)