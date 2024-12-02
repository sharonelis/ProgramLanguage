#ex2
# Write the shortest Python program, that accepts a list of strings and return a 
# single string that is a concatenation of all strings with a space between them. 
# Do not use the "join" function. Use lambda expressions. 

from functools import reduce
concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)

#test2
test_list = ["This", "is", "a", "test"]
print(concat_strings(test_list))  # Output: "This is a test"
