# The statistics module must be imported and its built-in functions used.
import statistics 
# Prompt the user to enter up to 10 numbers (integers or decimals) and store them in a list
user_floats = [] 
for i in range(10):  # Loop to get a maximum of 10 floats
    user_input = input(f"Enter number {i + 1} (integer or decimal, or press Enter to finish): ") 
    if user_input == "":
        break
    try:
        user_floats.append(float(user_input)) 
    except ValueError:
        print("Invalid input, please enter a valid float number.") 
# Determine the sum of the integers and print the outcome
if user_floats: 
    total_sum = sum(user_floats)  
    print(f"The sum of the entered floats is: {total_sum}")  
# Determine the maximum index and print the outcome.
    max_value = max(user_floats)  
    max_index = user_floats.index(max_value)  
    print(f"The maximum value is {max_value} at index {max_index}")  
# Determine the minimal index and print the outcome.
    min_value = min(user_floats)
    min_index = user_floats.index(min_value)
    print(f"The minimum value is {min_value} at index {min_index}") 
    mean_value = statistics.mean(user_floats)  # Calculate the mean of the floats
    print(f"The mean of the entered floats is: {round(mean_value, 2)}")
# Determine the median and print the outcome.
    median_value = statistics.median(user_floats)
    print(f"The median of the entered floats is: {median_value}") 