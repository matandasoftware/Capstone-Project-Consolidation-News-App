# pseudo code for a simple calculator app

# 1. Create a simple mathematical calculator app that can perform addition, subtraction, multiplication, and division.
# 2. the app should show a menu with options for either calculation, view saved equations, and exit the app.
# 3. if user choses to perform a calculation, prompt for two numbers and an operator.
# 4. perform the calculation based on the operator and display the result.
# 5. after the calculation display the result must be saved to a file equations.txt.
# 6. if the user chooses to view saved equations, read from the file and display the equations.

# python code

"""defining functions for the calculator app to perform basic arithmetic
 operations such as addition, subtraction, multiplication, and division respectively."""

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y
# function to save the equation to a file equations.txt
def save_equation(equation):
    with open("equations.txt", "a") as file:
        file.write(equation + "\n")
# function to view saved equations from the file equations.txt
def view_saved_equations():
    try:
        with open("equations.txt", "r") as file:
            equations = file.readlines()
            if equations:
                print("Saved Equations:")
                for eq in equations:
                    print(eq.strip())
# if no equations are saved print a message or the exception
            else:
                print("No saved equations found.")
    except FileNotFoundError:
        print("No saved equations found.")
# function to parse the input number and handle both int and float types
def parse_number(input_str):
#Try to parse input as int, fallback to float if needed
    try:
        if '.' in input_str:
            return float(input_str)
        else:
            return int(input_str)
    except ValueError:
        raise ValueError("Invalid input. Please enter a numeric value.")
    
""" This code defines a simple calculator app main menu
 asks the user to choose an option to perform a calculation,
 view saved equations, or exit the app."""

# main function to run the calculator app
def calculator_app():
    # This is the main loop of the calculator app
    while True:
        print("\nSimple Calculator App\nplease select an option which you'd like to perform:")
        print("1. Perform Calculation\n2. View Saved Equations\n3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            try:
                try:
                    # prompt user for two numbers and an operator
                    num1_str = input("Enter first number: ")
                    num1 = parse_number(num1_str)              # parse the first number
                    num2_str = input("Enter second number: ")
                    num2 = parse_number(num2_str)              # parse the second number
                except ValueError as e:
                    print(e)
                    continue
                # prompt user for an operator and perform the calculation
                print("Available operators: + to add, - to minus, * to multiply, / to divide")
                operator = input("Enter operator (+, -, *, /): ")
                if operator not in ['+', '-', '*', '/']:
                    raise ValueError("Invalid operator. Please choose from +, -, *, /.")
                if operator == '+':
                    result = add(num1, num2)
                elif operator == '-':
                    result = subtract(num1, num2)
                elif operator == '*':
                    result = multiply(num1, num2)
                elif operator == '/':
                    result = divide(num1, num2)
                # format the equation and save it to the file
                equation = f"{num1} {operator} {num2} = {result}"
                print(f"Result: {equation}")
                # save the equation to the file
                save_equation(equation)
            except ValueError as e:
                print(f"Error: {e}")
        # if user chooses to view saved equations, call the function to view them
        elif choice == '2':
            view_saved_equations()
        # if user chooses to exit the app, break the loop
        elif choice == '3':
            print("Exiting the calculator app.")
            break
        else:
            # if the user enters an invalid choice, print an error message
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    calculator_app()