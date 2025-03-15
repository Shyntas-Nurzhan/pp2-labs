x = int(input())
def squares():
    for i in range(x):
        yield (i+1)**2

for square in squares():
    print(square)