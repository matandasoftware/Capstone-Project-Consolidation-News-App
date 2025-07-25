# pseudo code

# 1. Write a program that continually asks the user to enter a number.
# 2. When the user enters “-1”, the program should stop requesting the user to request a number. 0 is not a valid number.
# 3. think of a way to exit the loop if the user enters -1
# 4. calculate the average of the valid numbers entered, excluding the -1 and 0.
# 5. Use a while loop to achieve the continuous prompting and number collection.

# python code

while True:
    num = int(input("Enter a number (-1 to stop): "))
    if num == -1:
        break  # Exit the loop if -1 is entered
    elif num == 0:
        continue  # Skip the rest of the loop if 0 is entered since it is not a valid number

    
    # calculate the average of valid numbers
    if 'total' not in locals():  # Initialize total and count if they don't exist
        total = 0                # Initialize total and count to zero
        count = 0
    total += num                 # Add the valid number to the total
    count += 1                   # Increment the count of valid numbers
if count > 0:
    average = total / count
    print(f"The average of the valid numbers is: {average}")
# If no valid numbers were entered
else:
    print("No valid numbers were entered to calculate an average.") 
