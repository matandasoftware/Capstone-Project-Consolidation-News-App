# pseudo code
# 1. white a syntax of a list to store the full names of my three friends
# 2. print out the name of the first friend, then the name of the last friend, and finally the length of the list.
# 3. define a list called friends_ages that stores the age of each of my friends respecftively of the names of my friends.
# 4. Print each friend’s name and age in a sentence 

# python code

"""create a list of friends' names, print the first and last names, and the length of the list."""

friends = ["Mufamadi Rofhiwa", "Mudau Khuliso", "Mufamadi Mulweli"]  
print(f"First friend: {friends[0]}")  
print(f"Last friend: {friends[-1]}")

# creating a list of friends' ages and printing each friend's name with their age

friends_ages = [25, 30, 22]  # create a list of friends' ages
# using enumerate of iterating through the list
for index, friend in enumerate(friends):
   print(f"{friend} is {friends_ages[index]} years old.")  # print each friend's name with their age

