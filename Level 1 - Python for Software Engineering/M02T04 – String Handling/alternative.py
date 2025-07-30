# pseudo code

# 1. Write a program that prompts the user to enter a string
# 2. makes each alternate character into an uppercase character and each other alternate character a lowercase character from the string.
# 3. Use a for loop to iterate through the string and change the case of each character.
# 4. Print the modified string after processing.
# 2. use the same string to make the alternative characters into lowercase and the other alternate characters into uppercase.
# 3. Use a for loop to iterate through the string and change the case of each character.
# 4. Print the modified string after processing.

# python code

input_string = input("Enter a string: ")                   # Prompt the user to enter a string
alternative_upp_low = ""                                   # Initialize an empty string to store the modified result
for i in range(len(input_string)):                         # Iterate through each character in the input string
    if i % 2 == 0:                                         # Check if the index is even
        alternative_upp_low += input_string[i].upper()     # Convert to uppercase for even indices
    else:
        alternative_upp_low += input_string[i].lower()     # Convert to lowercase for odd indices
print("alternative_upp-low:", alternative_upp_low)         # Print the modified string after processing of alternate characters

# now creating the opposite of the above print statement
alternative_low_upp = ""                                   # Initialize an empty string for the opposite case
for i in range(len(input_string)):
    if i % 2 == 0:                                         # Check if the index is even
        alternative_low_upp += input_string[i].lower()     # Convert to lowercase for even indices
    else:
       alternative_low_upp += input_string[i].upper()      # Convert to uppercase for odd indices
print("alternative_low-upp:", alternative_low_upp)         # Print the modified string after processing of opposite alternate characters

    
