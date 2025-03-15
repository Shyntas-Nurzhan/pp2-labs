import math 

def mult(nums):
    return math.prod(nums)

mylist = list(map(int, input().split()))

result = mult(mylist)

print(result)