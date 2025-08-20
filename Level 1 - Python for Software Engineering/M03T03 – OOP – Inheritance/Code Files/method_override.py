

# Age threshold for adulthood
ADULT_AGE = 18

# prompt for user inputs
name = input("Enter your name: ").strip()
age = int(input("Enter your age: "))
hair_color = input("Enter your hair color: ")
eye_color = input("Enter your eye color: ")

# Define the Adult and Child classes
class Adult:
    def __init__(self, name, age, hair_color, eye_color):
        self.name = name
        self.age = age
        self.hair_color = hair_color
        self.eye_color = eye_color

    def can_drive(self):
        # Adults are allowed to drive
        print(f"{self.name} is old enough to drive.")


class Child(Adult):


    def __init__(self, name, age, hair_color, eye_color):
        super().__init__(name, age, hair_color, eye_color)

    def can_drive(self):
        # Children are not allowed to drive
        print(f"{self.name} is too young to drive.")


# Only create and use the person object if running as the main script
if __name__ == "__main__":
    # Instantiate Adult or Child based on age
    if age >= ADULT_AGE:
        person = Adult(name, age, hair_color, eye_color)
    else:
        person = Child(name, age, hair_color, eye_color)
    # Print driving eligibility
    person.can_drive()






