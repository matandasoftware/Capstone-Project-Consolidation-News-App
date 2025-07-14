# autograded task 1

# pseudocde:
# 1. Create a string with exclamation marks
# 2. Replace exclamation marks with spaces
# 3. Print the modified string in uppercase
# 4. Print the modified string in reverse order

# python code:

"The!quick!brown!fox!jumps!over!the!lazy!dog."
print(single_string.replace("!", " "))          # replacing every exclamation mark with a blank space 
print(single_string.replace("!", " ").upper())  # printing the above string with spaces instead of exclamation marks in capital letters
print(single_string.replace("!", " ")[::-1])    # now using the slicing method, we can rewrite the string without exclamation marks backwards