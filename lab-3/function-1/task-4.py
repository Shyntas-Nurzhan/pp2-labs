def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    prime_numbers = []
    for number in numbers:
        if is_prime(number):
            prime_numbers.append(number)

    return prime_numbers

input_ = input("Enter numbers: ")

number_strings = input_.split()

numbers_list = []
for s in number_strings:
    numbers_list.append(int(s))

prime_list = filter_prime(numbers_list)

print(prime_list)