#ex8
# Write a one-line Python function that takes a list of integers and returns a new list 
# containing only the prime numbers, sorted in descending order. 
# Use lambda expressions and list comprehensions.

# Solution
#                                                                                                 # x = a*b, a <= b <= sqrt(x)
prime_numbers_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)

#test8
test_numbers = [3, 12, 7, 9, 11, 5, 16, 2]
print(prime_numbers_desc(test_numbers))  # Output: [11, 7, 5, 3, 2]
