import re

def matching(string):
    pattern = r'^a{1}.b{1}$'
    return bool(re.match(pattern, string))

txt = input()
x = matching(txt)

print(x)