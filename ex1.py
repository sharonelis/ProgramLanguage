#ex1
# Implement a Fibonacci sequence generator using a single lambda expression that 
# returns a list of the first n Fibonacci numbers. The function should take n as an input.

#The code uses the "reduce()" function to generate the Fibonacci sequence up to the nth number.
#The reduce function takes as an input a funcrion that takes two arguments, a list 
# and it can also take an initial value,
# and applies the function cumulatively to the list.

#The lambda function takes two arguments: x and _ (which is a placeholder).
#The first argument x represents the list of Fibonacci numbers generated so far.
#
#The lambda function appends the sum of the last two elements of x to the list x.
#The range function generates a sequence of numbers from 0 to n-2.
#The reduce function applies the lambda function to each element of the range and accumulates the result.
#The initial value of the list is [0, 1].
#Finally, the list is sliced to return only the first n elements.

from functools import reduce

fibonacci = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n-2), [0, 1])[:n]

#test1
print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

