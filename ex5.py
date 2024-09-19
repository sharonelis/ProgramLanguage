#ex5
from functools import reduce

sum_squared = reduce(lambda acc, x: acc + x, map(lambda x: x**2, filter(lambda num: num % 2 == 0, [1, 2, 3, 4, 5, 6])))

#test5
print(sum_squared)  # Output: 56
