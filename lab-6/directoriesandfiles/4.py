cnt = 0
f = open("text.txt", "r")

print(f.readline())

for x in f:
    cnt += 1

f.close()

print(cnt)