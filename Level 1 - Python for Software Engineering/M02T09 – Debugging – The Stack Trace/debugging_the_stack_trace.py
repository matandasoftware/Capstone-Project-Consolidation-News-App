# interpreting the stack trace

# creating a hypothesis steps

# 1. make observations
# 2. ask questions
# 3. make a hypothesis
# 4. make a prediction
# 5. test the hypothesis

# gaining visibility into code

# Function to count colours in a string that are separated by commas 
def count_red_green_blue(input_colors):
    red_count = 0 
    green_count = 0
    blue_count = 0 
    split_colors = input_colors.split(",")
    for color in split_colors: 
        if color == "red": 
            red_count += 1
        elif color == "green": 
            green_count += 1
        elif color == "blue": 
            blue_count += 1
    return f"Greens = {green_count}\nBlues = {blue_count}\nReds = {red_count}"
# Call function to count colours in a string and print result 
print(count_red_green_blue("green, red, green, green, blue, blue, blue"))

# outputing the values of the split_colors list with a print statement.

# Function to count colours in a string that are separated by commas 
def count_red_green_blue(input_colors): 
    red_count = 0 
    green_count = 0 
    blue_count = 0 
    split_colors = input_colors.split(",") 
    # Add a print statement to see the values in split_colors 
    print(split_colors)
    for color in split_colors: 
        if color == "red": 
            red_count += 1
        elif color == "green": 
            green_count += 1
        elif color == "blue": 
            blue_count += 1
    return f"Greens = {green_count}\nBlues = {blue_count}\nReds = {red_count}"
# Call function to count colours in a string and print result 
print(count_red_green_blue("green, red, green, green, blue, blue, blue"))

# adding a space to split correctly on the above
def count_red_green_blue(input_colors): 
    red_count = 0 
    green_count = 0 
    blue_count = 0 
    split_colors = input_colors.split(", ")  # Adding a space after the comma to split correctly
    # Add a print statement to see the values in split_colors 
    print(split_colors)
    for color in split_colors: 
        if color == "red": 
            red_count += 1
        elif color == "green": 
            green_count += 1
        elif color == "blue": 
            blue_count += 1
    return f"Greens = {green_count}\nBlues = {blue_count}\nReds = {red_count}"
# Call function to count colours in a string and print result 
print(count_red_green_blue("green, red, green, green, blue, blue, blue"))


