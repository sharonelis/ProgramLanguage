#ex8
is_prime = lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))
prime_numbers_desc = lambda lst: sorted([x for x in lst if is_prime(x)], reverse=True)

#test8
test_numbers = [3, 12, 7, 11, 5, 16, 2]
print(prime_numbers_desc(test_numbers))  # Output: [11, 7, 5, 3, 2]
