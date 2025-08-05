# Pseudocode:

# 1. Import required libraries
# 2. Define functions for investment and bond calculations
# 3. Implement a main function to manage user input and trigger the correct calculation
# 4. For Investment: calculate future value based on user input
# 5. For Bond: calculate monthly repayment or present value based on user input

# Python code:

# Main menu for investment and bond calculations
def main():
    print("Select 'Investment' or 'Bond' from the options below to continue:")
    print("Investment - calculate the interest earned on your investment.")
    print("Bond - calculate the repayment amount for a home loan.")

    # Ask user to select Investment or Bond
    choice = input("Enter your calculation type (Investment or Bond): ").strip().lower()
    
    # Call the relevant function based on user selection
    if choice == 'investment':
        investment_calculation()
    elif choice == 'bond':
        bond_calculation()
    else:
        print("Invalid choice. Please try again.")  # Display error for invalid input
    while True:
        choice = input("Enter your calculation type (Investment or Bond): ").strip().lower()
        if choice == 'investment':
            investment_calculation()
            break
        elif choice == 'bond':
            bond_calculation()
            break
        else:
            print("Invalid choice. Please try again.")

# Function to calculate investment value using simple or compound interest
def investment_calculation():
    print("Investment Calculation")
    while True:
        interest_type = input("Select 'simple' or 'compound' interest: ").strip().lower()
        if interest_type in ['simple', 'compound']:
            break
        else:
            print("Invalid interest type. Please try again.")

    # A: future value, P: principal, r: interest rate, t: years, n: compounding periods per year
    # Get principal, interest rate, duration, and compounding frequency from user
    while True:
        try:
            P = float(input("Enter the principal amount: "))
            r = float(input("Enter the annual interest rate (as a percentage): ")) / 100
            t = float(input("Enter the number of years: "))
            break
        except ValueError:
            print("Invalid entry. Please enter numeric values.")

    # Compute future value based on selected interest type
    if interest_type == 'simple':
        A = P * (1 + r * t)
    elif interest_type == 'compound':
        print("Compounding frequency options: 1 for annual, 12 for monthly, 4 for quarterly, etc.")
        while True:
            try:
                n = int(input("Enter the number of compounding periods per year (e.g., 1 for annual, 12 for monthly): "))
                if n > 0:
                    break
                else:
                    print("Please enter a positive integer for compounding frequency.")
            except ValueError:
                print("Invalid entry. Please enter a positive integer.")
        A = P * (1 + r / n) ** (n * t)
    print(f"The future value of the investment is: {A:.2f}")

def bond_calculation():  # Function to calculate bond repayment

    # p: present value, i: monthly interest rate, n: number of months

    print("Bond Calculation")
    # Get present value, interest rate, and repayment period from user
    while True:
        try:
            p = float(input("Enter the present value of the house: "))  # Get house value and convert to float
            i = float(input("Enter the monthly interest rate (as a percentage): ")) / 100 / 12  # Get interest rate, convert to monthly decimal
            n = int(input("Enter the number of months: "))  # Get repayment period in months
            break
        except ValueError:
            print("Invalid entry. Please enter numeric values.")

    # Calculate monthly repayment using the amortization formula:
    # repayment = (p * i) / (1 - (1 + i) ** -n)
    # where p = present value of the house, i = monthly interest rate, n = number of months.
    # This formula determines the fixed monthly payment required to pay off a loan over a specified period.
    repayment = (p * i) / (1 - (1 + i) ** -n)
    print(f"The monthly repayment on the bond is: {repayment:.2f}")  # Show result rounded to two decimals
    print(f"The monthly repayment on the bond is: {repayment:.2f}")  # Show result rounded to two decimals

if __name__ == "__main__":  # Run main function if script is executed directly
    main()
