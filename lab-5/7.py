import re

def snake_to_camel(txt):
    return re.sub(r'_([a-z])', lambda match: match.group(1).upper(), txt)

txt = input()
print(snake_to_camel(txt))