# pseudo code

# 1. a program that reads the data from the text file DOB.txt
# 2. and prints it out in two different sections one for the names and one for the dates of birth
# 3. the program should handle any errors that may occur while reading the file
# 4. the program should also handle cases where the file does not exist
# 5. the program should print an error message if the file cannot be read
# 6. the program should also handle cases where the file is empty
# 7. the program should print a message indicating that the file is empty if it is
# 8. the program should also handle cases where the file contains invalid data
# 9. the program should print a message indicating that the file contains invalid data if it does

# python code

"""obtaining the file DOB.txt's absolute path
 and verifying its existence; if not, printing an error message"""

import os
# checking if the file exists
file_path = os.path.join(os.path.dirname(__file__), "DOB.txt")                   # geting the absolute path to the file DOB.txt
if not os.path.exists(file_path):                                                # using os.path.exists to check if the file exists
    print("Error: The file does not exist.")                                     # handle case where file does not exist by printing an error message
   
    """If the file is located, open it in read mode using the open function,
     and handle any errors that may arise during the reading process with the try-except block.
       Display a notice stating that the file is empty if it is."""
else:
    try:
        with open(file_path, 'r') as file:                                 # opening the file in read mode 
            lines = file.readlines()                                       # read the lines from the file
            if not lines:                                                  # check if the file is empty
                print("The file is empty.")                                # handle case where file is empty by printing a message

                """Iterate through each line, divide them into names and birthdates, and print them under different parts if the file is not empty.
                One for names, and another for birth dates Print a notice stating that the file contains invalid data and end the loop if
                    the data does not have two parts for either the name or the date of birth."""
            else:                                                          # if the file is not empty, process the lines
                # split the lines into names and dates of birth
                names = []
                dates_of_birth = []
                valid_data = True
                for line in lines:
                    parts = line.strip().split(',')                         # split each line by comma
                    if len(parts) != 2:                                     # check if the line has exactly two parts which are name and date of birth
                        print("Invalid data found in the file.")            # handle case where line does not have exactly two parts
                        # when invalid data is found this sets valid_data to False then break out of the loop 
                        valid_data = False
                        break                                              
                    # if valid, append the name and date of birth to their respective lists
                    names.append(parts[0].strip())                          # append the name to names list by stripping whitespace
                    dates_of_birth.append(parts[1].strip())                 # append the date of birth to dates_of_birth list by stripping whitespace

                    """
                    if the valid data in the file is in two sections,apend the names and dates of birth in separate
                      sections and print the names and dates of birth under those separate sections. handle any error 
                      that may occur while reading or processing the file with a general exception
                    """
                if valid_data:  # print the names and dates of birth under separate sections one for names and one for dates of birth
                    print("Names:")
                    for name in names:
                        print(name)
                    print("\nDates of Birth:")
                    for dob in dates_of_birth:
                        print(dob)
    except Exception as e:  # handle any errors that may occur while reading or processing the file with a general exception
        print(f"An error occurred while reading the file: {e}")

        