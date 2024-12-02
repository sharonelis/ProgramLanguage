#ex5
# Rewrite the following program in one line by 
# using nested filter, map and reduce functions: 
    # nums = [1,2,3,4,5,6] 
    # evens = [] 
    # for num in nums: 
        # if num % 2 == 0: 
            # evens.append(num) 
    # squared = []  
    # for even in evens: 
        # squared.append(even**2) 
    # sum_squared = 0 
    # for x in squared: 
        # sum_squared += x 
    # print(sum_squared)

from functools import reduce

sum_of_squared_evens = reduce(lambda accumulator, x: accumulator + x, map(lambda x: x**2, filter(lambda num: num % 2 == 0, [1, 2, 3, 4, 5, 6])))

#test5
print(sum_of_squared_evens)  # Output: 56
