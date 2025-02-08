def unique(lst):
    unique_list = []
    for num in lst:
        if num not in unique_list:
            unique_list.append(num)
    return unique_list

numbers = input()

num_list = []
for num in numbers.split():
    num_list.append(int(num))

unique_list = unique(num_list)

print(unique_list)