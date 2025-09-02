# Pseudo Code

# Define a Shoe class to represent each shoe, storing country, code, product name, cost, and quantity.
# Use a list to store all Shoe objects as the main data structure.
# Key functions:
# - read_shoes_data(): Read shoe records from a file, validate them, and add them to the list.
# - capture_shoe(): Prompt the user for shoe details, validate input, and add a new Shoe to the inventory.
# - view_all_shoes(): Print all shoes in the inventory with their details.
# - restock_shoe(): Find the shoe with the lowest quantity, prompt for a restock amount, and update its quantity.
# - search_shoe(): Search for a shoe by its code and display the result.
# - calculate_value_per_item(): Calculate and display the total value (cost * quantity) for each shoe.
# - show_highest_quantity(): Display the shoe with the highest quantity, suggesting it for promotion.
# - main(): Provide a menu-driven interface for users to manage the shoe inventory interactively.
# Usage: Run the script and follow the menu prompts to manage your shoe inventory.



# python code

# Define the Shoe class with required attributes and methods
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return (
            f"{self.country}, {self.code}, {self.product}, "
            f"Cost: {self.cost}, Quantity: {self.quantity}"
        )


# List to store Shoe objects
shoe_list = []


# Reads shoe data from inventory.txt and populates shoe_list
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as file:
            next(file)  # Skip header
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    country, code, product, cost, quantity = parts
                    try:
                        shoe_list.append(Shoe(country, code, product, cost, quantity))
                    except ValueError:
                        print(f"Invalid data in line: {line.strip()}")
        print("Shoe data loaded successfully.")
    except FileNotFoundError:
        print("inventory.txt not found.")


# Captures new shoe details from user input
def capture_shoe():
    try:
        country = input("Enter country: ")
        code = input("Enter code: ")
        product = input("Enter product: ")
        cost = float(input("Enter cost: "))
        quantity = int(input("Enter quantity: "))
        shoe_list.append(Shoe(country, code, product, cost, quantity))
        print("Shoe added successfully.")
    except ValueError:
        print("Invalid input. Please enter valid cost and quantity.")


# Displays all shoes in the inventory
def view_all_shoes():
    for shoe in shoe_list:
        print(shoe)


# Finds shoe with lowest quantity and allows restocking
def restock_shoe():
    if not shoe_list:
        print("No shoes to restock.")
        return
    min_shoe = min(shoe_list, key=lambda s: s.quantity)
    print(f"Lowest quantity shoe: {min_shoe}")
    choice = input("Restock this shoe? (y/n): ")
    if choice.lower() == "y":
        try:
            add_qty = int(input("Enter quantity to add: "))
            min_shoe.quantity += add_qty
            print("Shoe restocked.")
        except ValueError:
            print("Invalid quantity entered.")


# Searches for a shoe by code
def search_shoe():
    code = input("Enter shoe code to search: ")
    found = False
    for shoe in shoe_list:
        if shoe.code == code:
            print(shoe)
            found = True
            break
    if not found:
        print("Shoe not found.")


# Calculates and displays value for each shoe
def calculate_value_per_item():
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        print(f"{shoe} - Total Value: {value}")


# Shows shoe with highest quantity
def show_highest_quantity():
    if not shoe_list:
        print("No shoes available.")
        return
    max_shoe = max(shoe_list, key=lambda s: s.quantity)
    print(f"Shoe for sale (highest quantity): {max_shoe}")


# Main menu loop
def main():
    while True:
        print("\nMenu:")
        print(
            "1. Read shoes data\n"
            "2. Capture new shoe\n"
            "3. View all shoes\n"
            "4. Restock shoe\n"
            "5. Search for shoe\n"
            "6. Calculate value per item\n"
            "7. Show highest quantity shoe\n"
            "8. Exit"
        )
        choice = input("Enter option (1-8): ")
        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            capture_shoe()
        elif choice == "3":
            view_all_shoes()
        elif choice == "4":
            restock_shoe()
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            calculate_value_per_item()
        elif choice == "7":
            show_highest_quantity()
        elif choice == "8":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
