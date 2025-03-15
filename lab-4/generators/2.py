n = int(input())
def even():
    for i in range(n+1):
        if (i%2==0):
            yield i
for num in even():
    print(num)