import time
import math

number = int(input())
delay = int(input())

time.sleep(delay / 1000)

sqrt = math.sqrt(number)

print(f"Square root of {number} after {delay} miliseconds is {sqrt}")