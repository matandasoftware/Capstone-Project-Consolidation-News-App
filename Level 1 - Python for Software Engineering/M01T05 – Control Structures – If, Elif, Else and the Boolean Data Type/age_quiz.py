# pseudocode: 

# 1. Write code to take in a user’s age and store it in an integer variable called age.
# 2. Assume that the oldest someone can be is 100; if the user enters a higher number, output the message: “Sorry, you're dead.”
# 3.If the user is 40 or over, output the message: “You're over the hill.”
# 4. f the user is 65 or older, output the message: “Enjoy your retirement!”
# 5. If the user is under 13, output the message: “You qualify for the kiddie discount.”
# 6. If the user is 21, output the message: “Congrats on your 21st!”
# 7. For any other age, output the message: “Age is but a number.”

# python code:

age = int(input("Please enter your age: "))         # prompt user for age and convert to integer
if age > 100:
    print("Sorry, you're dead.")                    # check if age is greater than 100 since 100 is assumed to be the oldest then print the appropriate message
elif age >= 40:
    print("You're over the hill.")                  # check if age is 40 or over  (against the specified conditions) and outputs the appropriate message
elif age >= 65:
    print("Enjoy your retirement!")                 # check if age is 65 or older (against the specified conditions) and outputs the appropriate message
elif age < 13:
    print("You qualify for the kiddie discount.")   # check if age is under 13 (against the specified conditions) and outputs the appropriate message
elif age == 21:
    print("Congrats on your 21st!")                 # check if age is 21 (against the specified conditions) and outputs the appropriate message
else:
    print("Age is but a number.")                   # for any other age except the above conditions, outputs appropriate message


