# pseudo code:

# 1. import the necessary libraries
# 2. define functions for investment and bond calculations
# 3. create a main function to handle user input and call the appropriate calculation function 
# 2. either Investment - to calculate the future value of an investment
# 3. or Bond - to calculate the amount you'll have to pay on a home loan.   
# 4. If the user chooses Investment, they should be prompted to enter either simple or compound interest, the principal amount, the interest rate, and the number of years. The program should then calculate and display the future value of the investment.
# 5. If the user chooses Bond, they should be prompted to enter the present value, interest rate, number of months, and whether they want to calculate the monthly repayment or the present value.

# python code:

# main menu for investment and bond calculations
def main():
    print("Choose either 'Investment' or 'Bond' from the menu below to proceed:")
    print("Investment - to calculate the amount of interest you'll earn on your investment.")
    print("Bond - to calculate the amount you'll have to pay on a home loan.")

    # prompt user to choose between Investment or Bond
    choice = input("Enter your calculation type (Investment or Bond ): ").strip().lower()                # and convert the input to lowercase to handle case insensitivity
    
    # call the appropriate function based on user choice
    if choice == 'investment':
        investment_calculation()
    elif choice == 'bond':
        bond_calculation()
    else:
        print("Invalid choice. Please try again.")                                           # If the user doesn’t type in a valid input, show an appropriate error message.
        main()

# function to calculate investment value based on simple or compound interest
def investment_calculation():
    print("Investment Calculation")
    interest_type = input("Choose 'simple' or 'compound' interest: ").strip().lower()        # and convert the input to lowercase to handle case insensitivity
    
    # If the user doesn’t type in a valid input, show an appropriate error message.
    if interest_type not in ['simple', 'compound']:
        print("Invalid interest type. Please try again.")
        investment_calculation()
        return
    
    #A is the future value of the investment, P is the principal amount, r is the interest rate and t is the number of years

    # request user input for principal, interest rate, and time period
    P = float(input("Enter the principal amount: "))                                     # prompt user to enter the principal amount and convert it to float
    r = float(input("Enter the interest rate (as a percentage): ")) / 100                # prompt user to enter the interest, Convert percentage to decimal and convert it to float            
    t = float(input("Enter the number of years: "))                                      # prompt user to enter the number of years and convert it to float

    # Calculate future value based on interest type
    if interest_type == 'simple':
        A = P * (1 + r * t)
    elif interest_type == 'compound':
        A = P * (1 + r) ** t
    else:
        print("Invalid interest type. Please try again.")                                # If the user doesn’t type in a valid input, show an appropriate error message.
        return
    print(f"The future value of the investment is: {A:.2f}")                             # Display the future value rounded to two decimal places

def bond_calculation():                                                                  # function to calculate bond repayment

    #p is the present value of the house, i is the monthly interest rate and n is the number of months

    print("Bond Calculation")
    # request user input for present value, interest rate, and number of months
    p = float(input("Enter the present value of the house: "))                             # prompt user to enter the present value of the house and convert it to float
    i = float(input("Enter the monthly interest rate (as a percentage): ")) / 100 / 12     # prompt user to enter the monthly interest rate, Convert percentage to decimal and convert it to float, then divide by 12 to get the monthly rate 
    n = int(input("Enter the number of months: "))                                         # prompt user to enter the number of months and convert it to an intiger 

# Calculate the monthly repayment using the formula
    repayment = (p * i) / (1 - (1 + i) ** -n)
    print(f"The monthly repayment on the bond is: {repayment:.2f}")                       # Display the monthly repayment rounded to two decimal places
if __name__ == "__main__":                                                                # This ensures that the main function is called when the script is run directly
    main() 