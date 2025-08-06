# import random module
import random
# Function to generate a random joke
def generate_joke():
    #Generates a random joke from a predefined list
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call cheese that isn't yours? Nacho cheese!"
    ]
    return random.choice(jokes)
# Main function to run the joke generator
def main():
    print("Welcome to the Joke Generator!")
# Prompt the user to press Enter to hear a joke or type 'exit' to quit
    while True:
        user_input = input("Press Enter to hear a joke or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print(generate_joke())
# Run the main function
if __name__ == "__main__":
    main()