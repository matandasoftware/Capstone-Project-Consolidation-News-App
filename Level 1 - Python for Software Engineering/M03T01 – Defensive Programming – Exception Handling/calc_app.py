
# Simple Calculator Application
# This script allows users to perform basic arithmetic operations, view saved equations, and exit the program.

import sys

def parse_number(input_str):
    """
    Convert the input string to an integer or float.
    Returns an int if the input is a whole number, or a float if it contains a decimal point.
    Raises ValueError if the input is not a valid number.
    """
    try:
        if '.' in input_str:
            return float(input_str)
        return int(input_str)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid input. Please enter an integer, a float (e.g., 5 or 3.14), or 'b' to return."
        )

def get_user_input(prompt):
    """
    Prompt the user for input and handle interruptions gracefully.
    Returns the user's input as a string, or None if input is interrupted.
    """
    try:
        return input(prompt)
    except EOFError:
        print("\nInput interrupted. Returning to main menu.")
        return None
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise

def calculate(x, y, operator):
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operators: +, -, *, /
    Raises ValueError for invalid operators or division by zero.
    """
    if operator == '+':
        return x + y
    if operator == '-':
        return x - y
    if operator == '*':
        return x * y
    if operator == '/':
        if y == 0:
            raise ValueError("Cannot divide by zero.")
        return x / y
    raise ValueError("Invalid operator. Supported operators are: +, -, *, /")

def save_equation(equation):
    """
    Save the given equation string to the 'equations.txt' file.
    Appends the equation to the file, creating it if it doesn't exist.
    """
    try:
        with open("equations.txt", "a", encoding="utf-8") as file:
            file.write(equation + "\n")
    except Exception as exc:
        print(f"Failed to save equation: {exc}")

def view_saved_equations():
    """
    Display all equations saved in the 'equations.txt' file.
    If the file does not exist or is empty, notifies the user.
    """
    try:
        with open("equations.txt", "r", encoding="utf-8") as file:
            equations = file.readlines()
            if equations:
                print("Saved Equations:")
                for eq in equations:
                    print(eq.strip())
            else:
                print("No saved equations found.")
    except FileNotFoundError:
        print("No saved equations found.")
    except Exception as exc:
        print(f"Error reading equations: {exc}")

def calculator_app():
    """
    Main loop for the calculator application.
    Presents a menu to the user to perform calculations, view saved equations, or exit.
    Handles user input and validation for all operations.
    """

    while True:
        try:
            print("\nSimple Calculator App\nPlease select an option:")
            print("1. Perform Calculation\n2. View Saved Equations\n3. Exit")
            choice_str = get_user_input("Choose an option (1-3): ")
            if choice_str is None:
                continue
            if not choice_str.isdigit():
                raise ValueError("Invalid input. Please enter a number (1-3).")
            choice = int(choice_str)
            if choice not in [1, 2, 3]:
                raise ValueError("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError as exc:
            print(f"Error: {exc}")
            print("Restarting program...\n")
            continue

        if choice == 1:
            # User chooses to perform a calculation
            # First number entry
            while True:
                num1_str = get_user_input(
                    "Enter first number (integer or decimal, or 'b' to return to main menu): "
                )
                if num1_str is None or num1_str.lower() == 'b':
                    break
                try:
                    num1 = parse_number(num1_str)
                except ValueError as exc:
                    print(exc)
                    continue

                # Second number entry
                while True:
                    num2_str = get_user_input(
                        "Enter second number (integer or decimal, or 'b' to return to main menu): "
                    )
                    if num2_str is None or num2_str.lower() == 'b':
                        break
                    try:
                        num2 = parse_number(num2_str)
                    except ValueError as exc:
                        print(exc)
                        continue

                    # Operator entry
                    while True:
                        operator = get_user_input("Enter operator (+, -, *, /): ")
                        if operator in ['+', '-', '*', '/']:
                            try:
                                result = calculate(num1, num2, operator)
                                equation = f"{num1} {operator} {num2} = {result}"
                                print(f"Result: {equation}")
                                save_equation(equation)
                            except Exception as exc:
                                print(f"Calculation error: {exc}")
                            break
                        else:
                            print("Invalid operator. Please enter one of: +, -, *, /")
                    break  # Exit second number entry after calculation
                break  # Exit first number entry after calculation

        elif choice == 2:
            # User chooses to view saved equations
            view_saved_equations()
        elif choice == 3:
            # User chooses to exit the application
            print("Exiting the calculator app. Goodbye!")
            sys.exit(0)

        if choice == 1:
            # User chooses to perform a calculation
            # First number entry
            while True:
                num1_str = get_user_input("Enter first number (integer or decimal, or 'b' to return to main menu): ")
                if num1_str is None or num1_str.lower() == 'b':
                    break
                try:
                    num1 = parse_number(num1_str)
                except ValueError as e:
                    print(e)
                    continue

                # Second number entry
                while True:
                    num2_str = get_user_input("Enter second number (integer or decimal, or 'b' to return to main menu): ")
                    if num2_str is None or num2_str.lower() == 'b':
                        break
                    try:
                        num2 = parse_number(num2_str)
                    except ValueError as e:
                        print(e)
                        continue

                    # Operator entry
                    while True:
                        operator = get_user_input("Enter operator (+, -, *, /): ")
                        if operator in ['+', '-', '*', '/']:
                            try:
                                result = calculate(num1, num2, operator)
                                equation = f"{num1} {operator} {num2} = {result}"
                                print(f"Result: {equation}")
                                save_equation(equation)
                            except Exception as e: 
                                print(f"Calculation error: {e}")
                            break
                        else:
                            print("Invalid operator. Please enter one of: +, -, *, /")
                    break  # Exit second number entry after calculation
                break  # Exit first number entry after calculation

        elif choice == 2:
            # User chooses to view saved equations
            view_saved_equations()
        elif choice == 3:
            # User chooses to exit the application
            print("Exiting the calculator app. Goodbye!")
            sys.exit(0)



# Entry point for the script
if __name__ == "__main__":
    calculator_app()
