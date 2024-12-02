#ex6
# Write one-line function that accepts as an input a list of lists containing strings 
# and returns a new list containing the number of palindrome strings in each sublist. 
# Use nested filter / map / reduce functions. 

from functools import reduce

palindrome_count = lambda lst: list(map(lambda sublist: reduce(lambda palindrome_counter, str: palindrome_counter + 1 if str == str[::-1] else palindrome_counter, sublist, 0), lst))

#test6
test_lists = [["madam", "test", "level"], ["abc", "racecar", "12321"], ["not", "a", "palindrome"]]
print(palindrome_count(test_lists))  # Output: [2, 2, 1]
