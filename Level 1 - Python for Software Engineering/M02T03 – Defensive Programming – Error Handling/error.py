# pseudo code

# 1. white a profgram that gets error messages, fix them and name the type of error
# 2. The program should handle different types of errors such as ValueError, TypeError, etc.
# 3. Use try-except blocks to catch and handle the errors.
# 4. Print a message indicating the type of error encountered.
#5. askng the user to input a mass and heat value, then process them if they are valid.

# python code

try:
    mass = float(input("Enter the mass: "))
    heat = float(input("Enter the heat: "))
except ValueError as e:
    print(f"ValueError: {e}. Please enter valid numbers for mass and heat.")    # Handle ValueError if input is not a number
except TypeError as e:
    print(f"TypeError: {e}. Please ensure you are entering numbers.")           # Handle TypeError if the input type is incorrect
except Exception as e:
    print(f"An unexpected error occurred: {e}. Please try again.")              # Handle any other unexpected errors
if mass > 0 and heat > 0:
    # process or add to answers
    print("Processing the mass and heat values...")
else:
    print("Mass and heat must be greater than zero. Please enter valid values.")
# If no valid numbers were entered
   
  