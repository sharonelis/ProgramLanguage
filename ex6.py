#ex6
from functools import reduce

palindrome_count = lambda lst: list(map(lambda sublist: reduce(lambda acc, s: acc + 1 if s == s[::-1] else acc, sublist, 0), lst))

#test6
test_lists = [["madam", "test", "level"], ["abc", "racecar", "12321"], ["not", "a", "palindrome"]]
print(palindrome_count(test_lists))  # Output: [2, 2, 1]
