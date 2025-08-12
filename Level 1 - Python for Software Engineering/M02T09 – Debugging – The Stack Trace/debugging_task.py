import random
guess = ""
while guess not in ("heads", "tails"):
    print("Guess the coin toss! Enter heads or tails:")
    guess = input()
# Fixed missing colon at end of while statement

toss = random.randint(0, 1) # 0 is tails, 1 is heads

# Convert guess to 0 or 1 for comparison
if guess == "heads":
    guess_num = 1
else:
    guess_num = 0
# Added conversion from string guess to integer for comparison

if toss == guess_num:
    print("You got it!")
else:
    print("Nope! Guess again!")
    guess = input()
    if guess == "heads":
        guess_num = 1
    else:
        guess_num = 0
    # Added conversion for second guess as well

    if toss == guess_num:
        print("You got it!")
    else:
        print("Nope. You are really bad at this game.")