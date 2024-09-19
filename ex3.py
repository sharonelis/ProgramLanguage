#ex3
from functools import reduce

cumulative_sum_of_squares = lambda lst: list(map(
    lambda sublist: reduce(
        lambda acc, x: acc + (lambda n: n**2)(x),
        filter(lambda y: y % 2 == 0, sublist),
        0
    ), lst
))

#test3
test_lists = [[2, 3, 4], [1, 6, 8], [5, 7, 2, 10]]
print(cumulative_sum_of_squares(test_lists))  # Output: [20, 100, 104]
