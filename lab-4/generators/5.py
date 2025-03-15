n = int(input())

def AbsoluteZero():
    for i in range(n+1):
        yield n - i

for num in AbsoluteZero():
    print(num)