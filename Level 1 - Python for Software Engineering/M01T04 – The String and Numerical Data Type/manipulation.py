# autograded task 2

# pseudocode:
# 1. Request a string input from the user
# 2. Print the length of the string
# 3. Replace the last character of the string with '@'
# 4. Print the last three words of the string
# 5. Create a new string with the first three words and the last two words of the original string

# python code:

str_manip = input("Enter a string: ")                    # requesting user input of a string and storing it in a variable str_manip
print(f"The length of the string is: {len(str_manip)}")  # any entered string length's display given by the len() function
print(replace(str_manip[-1], "@"))                       # find the last letter of the string and replace it with @  
print(str_manip.split()[-3:])                            # geting the last three words of the string and printing them backwards
print((str_manip.split()[:3] + str_manip.split()[-2:]))  # creating a five-letter words with the first three words and the last two words of the string