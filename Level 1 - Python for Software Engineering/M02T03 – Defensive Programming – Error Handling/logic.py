# pseudo code

# 1. define a function that that takes the mass of a rocket in kg and the heat generated in kJ
# 2. calculates the speed of the rocket in m/s using the formula speed = sqrt(2 * heat / mass)
# 3. returns the speed in m/s
# 4. handle exceptions for invalid inputs (e.g., negative mass or heat)
# 5. takes the calculated speed and calculates the kinetic energy using the formula KE = 0.5 * mass * speed^2 
# 6. returns the kinetic energy in kJ
# 7. handle exceptions for invalid inputs (e.g., negative speed)
# 8. print the results in a formatted string
# 9. and prints the exception message if any error occurs

# python code

"""importing necessary libraries, in this case, math for mathematical operations
defining the function to calculate speed in m/s given the rocket values of the mass 
in kg and heat in kJ, and handling exceptions for invalid inputs on the formula for speed"""

import math
def calculate_speed(mass, heat):
    if mass <= 0:
        raise ValueError("Mass must be greater than 0.")
    if heat < 0:
        raise Exception("Heat is lost to the environment, it cannot be negative.")
    
    speed = math.sqrt(2 * heat / mass)                                                                               # formula for speed
    return speed

""" defining the function to calculate kinetic energy in kJ given the mass in kg and speed in m/s,
and handling exceptions for invalid inputs on the formula for kinetic energy"""

def calculate_kinetic_energy(mass, speed):
    if speed < 0:
        raise ValueError("Speed cannot be negative.")
    
    kinetic_energy = 0.5 * mass * speed ** 2                                                                         # formula for kinetic energy
    return kinetic_energy

"""main block to execute the functions with various test cases, including valid and invalid inputs which the errors are 
caught and printed as exception messages for the rocket with the mass of 1500 kg and heat of -20000 kJ, andthe rocket of 
mass -500 kg and heat of 30000 kJ,printing the results in a formatted string"""

for mass, heat in [(1000, 50000), (2000, 100000), (-500, 30000), (1500, -20000)]:                                    # four different rockets with different mass and heat values
    # using try-except to handle exceptions for each rocket
    try:
        speed = calculate_speed(mass, heat)
        kinetic_energy = calculate_kinetic_energy(mass, speed)
        print(f"Mass: {mass} kg, Heat: {heat} kJ, Speed: {speed:.2f} m/s, Kinetic Energy: {kinetic_energy:.2f} kJ")   # formatted string for output
    except Exception as err:
        print(f"Mass: {mass} kg, Heat: {heat} kJ, Exception: {err}")                                                  # converting the exception to string for output



