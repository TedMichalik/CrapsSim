# Author:  Ted Michalik
# Version: 1.0
# Date:    10/20/18
import time, craps_methods
from datetime import date
import matplotlib.pyplot as plt

# ----------------Display build version and local time---------------------
today = date.today()
build_version = 1.0
current_time = time.asctime(time.localtime(time.time()))
print("\n\nBuild Version:", str(build_version), "\nTime:", str(current_time), "\n\n")
# -------------------------------------------------------------------------


def WinFrequency():
    """Creates win amount frequency chart for Craps strategy"""
    sessions = 1000000 # Number of 100 game sessions to run
    x = [] # Net gain
    y = [] # Number of times that amount was won or lost
    TotalLost = 0
    TotalWon = 0
    MaxWin = 0

    for s in range(sessions):
        won, lost = PassWithOdds(100, False)
        gain = won - lost
        if gain in x:
            i = x.index(gain)
            y[i] += 1
        else:
            x.append(gain)
            y.append(1)
        TotalLost += lost
        TotalWon += won
        if won > MaxWin:
            MaxWin = won
    edge = (1 - TotalWon / TotalLost) * 100
    edge = round(edge, 2)
    current_time = time.asctime(time.localtime(time.time()))
    print("Calculations complete.\nTime:", str(current_time), "\n\n")
    print("For", sessions, "sessions: Max Win =", MaxWin)
    print("Total Lost =", TotalLost, ", Total Won =", TotalWon, ", House Edge =", edge, "%")
    plt.scatter(x, y, color = 'green', s=10)
    plt.xlabel('Net Gain')
    plt.ylabel('No. of sessions (100 Games per Session)')
    plt.title('Net Gain Frequency - Pass Line, Max Odds')
    plt.text(0, 0, "Pot=2000\nSessions={:,}\nHouse Edge={:.2%}\nAvg Loss per Session={:.2f}".format(sessions, 1-TotalWon/TotalLost, (TotalLost-TotalWon)/sessions),
             horizontalalignment='center')
    plt.show()


def DiceFrequency(rolls):
    """Creates dice frequency chart to confirm proper randomness"""
    dice = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # Possible dice rolls
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Number of times that roll occured
    c = craps_methods.CrapsGame(5, 300, True, False)
    for t in range(rolls):
        c.shooter_rolls()
        if c.dice in dice:
            y[dice.index(c.dice)] += 1
        else:
            print("Dice value is invalid:", c.dice)
            break
    # plotting a bar chart
    plt.bar(dice, y, color = 'green') 
    # x-axis label 
    plt.xlabel('dice') 
    # frequency label 
    plt.ylabel('No. of rolls') 
    # plot title 
    plt.title('Dice Frequency') 
    # function to show the plot 
    plt.show()


def crapsTestSim(numGames):
    """Plays numGames consecutive games for testing purposes"""
    minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
    starting_pot = 300  # Starting amount with which to bet
    right_way = True  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
    working = True  # While shooter retains dice, i.e. throws a point, keep any Come/Don't Come Bet Odds working on the Opening Roll
    print_results = True  # Print results of each roll; good to use while testing

    c = craps_methods.CrapsGame(minimum_bet, starting_pot, working, print_results)

    for t in range(numGames):
        c.rollCount = 0
        c.point = 0
        c.resolved = False

        c.add_bet("Pass", minimum_bet, right_way) # True = bet "Do" Pass/Come side; False = bet "Don't" Pass/Come side
        c.add_bet("Field", minimum_bet, True)

        while not c.resolved:
            c.shooter_rolls()
            if c.rollCount == 1:
                max_odds = Odds3_4_5x(c.point, minimum_bet, right_way)
                c.set_odds("Pass", max_odds, c.point, right_way)
    else:
        print("Starting Pot =", starting_pot, "Total Won =", c.total_won, "Total Lost =", c.total_lost, "Final Pot Amount =", c.pot_amount)


def PassWithOdds(numGames, print_status):
    """Plays numGames consecutive with Pass line bet and max odds"""
    minimum_bet = 5  # Minimium bet to place on the Pass/Don't Pass & Come/Don't Come lines
    starting_pot = 2000  # Starting amount with which to bet
    right_way = True  # True = bet "Do"/Pass/Come side; False = bet "Don't" Pass/Come side
    print_results = print_status  # Print results after all games complete
    """ Plotting Data """
    x = [] # Game number
    y = [] # Pot amount after each game

    c = craps_methods.CrapsGame(minimum_bet, starting_pot, False, False)

    for t in range(numGames):
        c.rollCount = 0
        c.point = 0
        c.resolved = False
        if print_results:
            print("After game", t, ", the pot amount is", c.pot_amount)
        x.append(t)
        y.append(c.pot_amount)
        if c.pot_amount <= 0:
            won = c.total_won
            lost = c.total_lost
            SessionResults(t, c.pot_amount, won, lost, x, y, print_results)
            return won, lost

        # Place bets for the Come out roll here.
        c.add_bet("Pass", minimum_bet, right_way) # True = bet "Do" Pass/Come side; False = bet "Don't" Pass/Come side

        while not c.resolved:
            c.shooter_rolls()
            if c.rollCount == 1:
                # Pass line Point set. Place bets here.
                max_odds = Odds3_4_5x(c.point, minimum_bet, right_way)
                c.set_odds("Pass", max_odds, c.point, right_way)
    else:
        t += 1
        won = c.total_won
        lost = c.total_lost
        x.append(t)
        y.append(c.pot_amount)
        SessionResults(t, c.pot_amount, won, lost, x, y, print_results)
        return won, lost


def Odds3_4_5x(point, bet, right_way):
    if not right_way:
        max_odds = 6 * bet
    else:
        if point in [4,10]:
            max_odds = 3 * bet
        elif point in [5,9]:
            max_odds = 4 * bet
        elif point in [6,8]:
            max_odds = 5 * bet
    return max_odds

        
def SessionResults(t, pot, won, lost, x, y, print_results):
    if print_results:
        print("After game", t, ", the pot amount is", pot)
        print("Total won =", won, "Total lost =", lost)
        plt.plot(x, y)
        plt.xlabel('Game')
        plt.ylabel('Pot Amount')
        plt.title('Craps Session History - Pass with max odds')
        plt.show()
    pass



#crapsTestSim(5)
#won, lost = PassWithOdds(100, True)
WinFrequency()
#DiceFrequency(1000000)
