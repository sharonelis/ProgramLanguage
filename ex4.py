#ex4
# Write a higher-order function that takes a binary operation (as a lambda function) 
# and returns a new function that applies this operation cumulatively to a sequence. 
# Use this to implement both factorial and exponentiation functions.

def cumulative_operation(operation): # it's like the reduce function
    def apply_operation(sequence):
        result = sequence[0] # Initialize the result with the first element
        for num in sequence[1:]: # Apply the operation to the rest of the elements
            result = operation(result, num) # Update the result
        return result # Return the final result
    return apply_operation # Return the function that applies the operation

# Factorial: using multiplication as the operation
factorial = cumulative_operation(lambda x, y: x * y)

# Exponentiation: usuing multiplication as the operation
exponentiation = cumulative_operation(lambda x, y: x ** y)

#test4
# Testing factorial
print(factorial([1, 2, 3, 4, 5]))  # Output: 120 (5!)
# Testing exponentiation
print(exponentiation([2, 4]))  # Output: 16 (2^4)
