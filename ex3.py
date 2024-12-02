#ex3
# Write a Python function that takes a list of lists of numbers and return a new list 
# containing the cumulative sum of squares of even numbers in each sublist.  
# Use at least 5 nested lambda expressions in your solution.  

from functools import reduce

cumulative_sum_of_squares = lambda lst: list(map(
    lambda sublist: reduce(
        lambda accumulator, x: accumulator + (lambda n: n**2)(x),
        filter(lambda y: y % 2 == 0, sublist),
        0
    ), lst
))

#test3
test_lists = [[2, 3, 4], [1, 6, 8], [5, 7, 2, 10]]
print(cumulative_sum_of_squares(test_lists))  # Output: [20, 100, 104]


