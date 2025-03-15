string = input()

uppercase = sum(1 for char in string if char.isupper())

lowercase = sum(1 for char in string if char.islower())

print("Upper: ", uppercase)
print("Lower: ", lowercase)