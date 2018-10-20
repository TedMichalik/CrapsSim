import random

def rollDice(die1,die2,dice,rollCount,print_results):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        dice = die1 + die2
        rollCount = rollCount + 1
        if print_results:
            print("You roll a", die1, "and", die2, "for a total of", dice)

