def permutate(word):
    if len(word) <= 1:
        return word
    permutations = []

    for i in range(len(word)):
        char = word[i]
        remaining = word[:i] + word[i+1:]

        for perm in permutate(remaining):
            permutations.append(char + perm)
    return permutations

input_ = input("Print a word: ")
result = permutate(input_)

print(result)