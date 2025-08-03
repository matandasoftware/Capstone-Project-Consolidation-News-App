# pseudo code

# 1. a program that allow user to register students for an exam venue
# 2. the program should ask the user how many students they want to register
# 3. a for loop for the number of students
# 4. inside the loop, ask for the next student id number
# 6. write each id number to a text file called reg_form.txt
# 8. Include a dotted line after each student ID for a signature during attendance

# python code

import os  
# defining the function to register students
def register_students():

    """using try-except block to handle invalid input for number of students
    if the input is not a valid integer, print an error message and return
    if the input is a valid integer, proceed to register the students""" 
    
    try:
        num_students = int(input("How many students do you want to register? "))    # prompt user to specify how many students to register
        if num_students <= 0:                                                       # check if the number of students is a positive integer if not print an error message and return
            print("Please enter a positive number.")
            return
    except ValueError:                                                              # handle case where input is not a valid integer by catching ValueError and printing an error message then returning
        print("Invalid input. Please enter a valid number.")
        return

    """To add student IDs, make sure the file reg_form.txt is present and open it in append mode,
    To add new content to a file without erasing current content, use the 'a' mode,After another
     student's ID is entered, write each ID to the file with a line of 20 dots for signature during attendance,
    This is done by iterating through the number of students the user requested using the for loop """

    # open the file in append mode
    with open("reg_form.txt", "a") as file:
        for i in range(num_students):                                               # iterate through the number of students
            student_id = input(f"Enter ID number for student {i + 1}: ")            # save the student ID input to a variable
            file.write(student_id + "\n")                                           # write the student ID to the file as a new line for each student
            file.write("-" * 20 + "\n")                                             # adding 20 dotted lines ater each ID for signature upon attendance

    print(f"{num_students} students registered successfully.")                      # formatting the output message to indicate successful registration for the specified number of students

# Call the function to execute the registration process
register_students()