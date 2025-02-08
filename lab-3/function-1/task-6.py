def reversed(sentence):
    return " ".join(reversed(sentence.split()))

input_ = input("Enter a sentence: ")
print(reversed(input_))