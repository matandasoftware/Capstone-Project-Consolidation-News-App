# pseudocode:

# 1. request competetator's times for each of the trithlon events namely swimming, cycling, and running and 
# 2. store them in variables and print each time in variable format
# 4. calculate the total time for each competitor by adding the times of swimming, cycling, and running and print the total time
# 3. use the qualifying criteria with its corresponding time range to determine the award category
# 4. print the award category based on the total time

# python code:

swim = int(input("Enter time taken for swimming in minutes : "))       # asking user to input time taken for swimming in minutes and storing it in a variable swim in an integer format and printing it
print("Time taken for Swimming task: ",swim)

cycl = int(input("Enter time taken for cycling in minutes : "))        # asking user to input time taken for cycling in minutes and storing it in a variable cycl in an integer format and printing it
print("Time taken for Cycling task: ",cycl)

run = int(input("Enter time taken for running in minutes : "))         # asking user to input time taken for running in minutes and storing it in a variable run in an integer format and printing it
print("Time taken for Running task: ",run)

Total_time=swim+cycl+run
print("Total time taken for triathlon: ",Total_time)                   # calculating total time taken for triathlon by adding swim, cycl and run intigers

# Output the award they will receive or ‘No award’
print("Award: ", end="")                                       # printing the award received based on the qualifying criteria time range
if (Total_time < 100):                                  
    print("Provincial Colors")                                         # using qualifying criteria time range print received award category if criteria is met
elif (Total_time > 100 and Total_time <=105):           
    print("Provincial Half Colors")                                    # using qualifying criteria time range print received award category if criteria is met
elif (Total_time >105 and Total_time <=110):
    print("Provincial Scroll")                                         # using qualifying criteria time range print received award category if criteria is met
else:
    print("No award")                                                  # using qualifying criteria time range print received award category if criteria is met
