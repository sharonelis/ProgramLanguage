#ex4
def cumulative_operation(operation):
    def apply_operation(sequence):
        result = sequence[0]
        for num in sequence[1:]:
            result = operation(result, num)
        return result
    return apply_operation

# Factorial: using multiplication as the operation
factorial = cumulative_operation(lambda x, y: x * y)

# Exponentiation: calculate base^exp
def exponentiation(base, exp):
    return base ** exp

#test4
# Testing factorial
print(factorial([1, 2, 3, 4, 5]))  # Output: 120 (5!)
# Testing exponentiation
print(exponentiation(2, 4))  # Output: 16 (2^4)
