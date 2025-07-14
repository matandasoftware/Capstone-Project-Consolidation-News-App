# autograded task 3

# pseudocode:
# 1. Request three integer inputs from the user
# 2. Print each integer
# 3. Print the sum of all three integers
# 4. Print the first integer minus the second integer
# 5. Print the third integer multiplied by the first integer
# 6. Print the sum of all three integers divided by the third integer

# python code:

intiger1 = input("Enter a number: ")  # asking user to  input intiger and store it in a variable intiger1
intiger2 = input("Enter a number: ")  # asking user to  input intiger and store it in a variable intiger2
intiger3 = input("Enter a number: ")  # asking user to  input intiger and store it in a variable intiger3
# printing individual intigers entered  by the user
print(f"first number: {intiger1}")    # printing first intiger
print(f"second number: {intiger2}")   # printing second intiger
print(f"third number: {intiger3}")    # printing third intiger


print(f"first number + second number + third number: {int(intiger1) + int(intiger2) + int(intiger3)}")                                     # the sum of all intigers by user, all three intigers by first converting them to int and adding them
print(f"first number - second number: {int(intiger1) - int(intiger2)}")                                                                    # the first number minus the second number by first converting the first and second intigers to int and subtracting them
print(f"third number * first number: {int(intiger3) * int(intiger1)}")                                                                     # the third number multiplied by the first number by first converting the third and first intigers to int and multiplying them
print(f"(first number + second number + third number) / third number: {(int(intiger1) + int(intiger2) + int(intiger3)) / int(intiger3)}")  # the sum of all three numbers divided by the third number by first converting all three intigers to int and dividing them