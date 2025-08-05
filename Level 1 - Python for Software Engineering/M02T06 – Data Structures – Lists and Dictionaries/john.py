# pseudo code

# 1. while the entered string is not john
# 2. create a list of strings entered by the user called incorrect names
# 3. if the entered string is john, print "Hello John"

# python code

incorrect_names = []  # initialize an empty list to store incorrect names
while True:
    name = input("Enter your name: ") # Prompt user for input
    if not name.isalpha(): # Check if the name contains only alphabetic characters
        print("Name must contain only alphabetic characters.") # print error message for invalid characters
        continue # Continue to the next iteration if invalid input
    if name.lower() == "john": # Check if the entered name is "john" (case insensitive)
        break
    incorrect_names.append(name) # Add the incorrect name to the list
print("incorrect_names:", incorrect_names) # Print the list of incorrect names


