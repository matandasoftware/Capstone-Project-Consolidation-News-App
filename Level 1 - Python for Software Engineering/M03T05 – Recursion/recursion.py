# recursive functions

# let's take a function of cutting a cake into slices 

def cut_cake(number_of_friends, number_of_slices): 
    # Cut cake in half 
    number_of_slices = number_of_slices * 2

# Check if there are enough slices for everybody 
    if number_of_slices >= number_of_friends: # Base case 
        # If there are enough slices - return the number of slices 
        return number_of_slices

    else: # If there are not enough slices - cut the resulting 
          # slices in half again 
        return cut_cake(number_of_friends, number_of_slices)

print(cut_cake(11, 1))

# FACTORIALS AND RECURSION

# defining the factorial of a number n recusively by 
# 0! = 1
# n! = n × (n − 1)! where n > 0

# the recursive function of calculating n is shown below

def factorial(n): 
    # Base case: if n is 0, return 1 because 0! is defined as 1 
    if n == 0: 
        return 1
    else: 
        # Recursive case: calculate n! by multiplying n with the factorial 
        # of (n - 1)
        return n * factorial(n - 1)

print(f"The factorial of 4 is {factorial(4)}")

# in summary, a recursive function must have:
# 1. A base case that stops the recursion
# 2. A recursive case that breaks the problem down into smaller subproblems
# 3. Each recursive call should bring the function closer to the base case
# 4. Proper handling of inputs to avoid infinite recursion
# 5. Consideration of performance and stack depth for large inputs
# 6. Clear and concise code for readability and maintainability
# 7. Testing with various inputs to ensure correctness and robustness
# 8. Understanding of the problem domain to effectively apply recursion

# RECURSION IN PYTHON

# To view the recursion limit, do the following: 
from sys import getrecursionlimit
print(getrecursionlimit()) # Value printed would be 1000 by default

# To change the recursion limit, do the following: 
from sys import getrecursionlimit, setrecursionlimit
setrecursionlimit(2000) 
print(getrecursionlimit()) # Value printed will now be 2000

