# pseudo code

# 1. a list called menu for items sold in the cafe
# 2. stock value for each item in the menu
# 3. a dictionary called stock with items as keys and stock values as values
# 4. a dictionary called price with items as keys and prices as values
# 5. store the value in a variable called total_stock

# python code

menu = ["coffee", "tea", "sandwich", "cake"]  # List of items sold in the cafe
stock_value = [10, 20, 15, 5]  # Stock value for each item in the menu
stock = dict(zip(menu, stock_value))  # Create a dictionary with items as keys and stock values as values
prices = [2.5, 1.5, 5.0, 3.0]  # Prices for each item in the menu
price = dict(zip(menu, prices))  # Create a dictionary with items as keys and prices as values
total_stock = sum(stock[item] * price[item] for item in menu)  # Calculate the total stock value
print ("Total stock:", total_stock)  # Print the total stock value

