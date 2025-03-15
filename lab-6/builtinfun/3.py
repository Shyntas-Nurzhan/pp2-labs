def is_palindrome(s):
    return s == s[::-1]

text = input()

if is_palindrome(text):
    print("Is palindrome")
else:
    print("Is not palindrome")