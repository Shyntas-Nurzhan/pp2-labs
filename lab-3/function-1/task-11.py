def is_palindrome(word):
    word = word.lower()
    return word == word[::-1]

user_input = input("Enter a word: ")
if is_palindrome(user_input):
    print("Yes")
else:
    print("No")