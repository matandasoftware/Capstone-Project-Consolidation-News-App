

# Parent class representing a general course
class Course:
    """Base class for courses."""
    name = "Fundamentals of Computer Science"
    contact_website = "www.hyperiondev.com"

    def head_office(self):
        print("Head office is located in Cape Town, South Africa")

    def contact_details(self):
        # Print contact website for the course
        print("Please contact us by visiting", self.contact_website)



# Subclass for a specific OOP course
class OOPCourse(Course):
    """Subclass for OOP course."""

    def __init__(self, description, trainer):
        # Store course description and trainer name
        self.description = description
        self.trainer = trainer

    def trainer_details(self):
        # Print course description and trainer
        print(f"This course is about: {self.description}")
        print(f"Trainer: {self.trainer}")

    def show_course_id(self):
        # Print a fixed course ID
        print("Course ID: #12345")




# Instantiate OOPCourse and display all required details
course_1 = OOPCourse("OOP Fundamentals", "Mr Anon A. Mouse")
course_1.contact_details()
course_1.trainer_details()
course_1.show_course_id()