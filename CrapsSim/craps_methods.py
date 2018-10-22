import random

class CrapsGame(object):
    def __init__(self, min_bet, odds_bet, start_amount, right_way, working, print_results):
        """Passed variables"""
        self.min_bet = min_bet  # amount bet (int) on pass/don't pass line, come/don't come line
        self.odds_bet = odds_bet  # amount (int) that can be bet "behind the pass/don't pass or come/don't come line"
        self.start_amount = start_amount  # $ amount with which one walks up to table
        self.pot_amount = start_amount  # track $$ left in pot after each shooter roll
        self.right_way = right_way  # track whether to bet on Do or Don't side
        self.working = working  # track whether or not to let Come Odds "work" on the Come Out roll (Don't Come Odds always ON)
        self.print_results = print_results # True/False whether to print roll by roll stats (for testing)
        """Object tracking variables"""
        self.line_bets = []  # list of LineBet objects to track Pass & Come Line bets
        self.die1 = 0
        self.die2 = 0
        self.dice = 0
        self.rollCount = 0
        self.point = 0

    def add_line_bet(self, min_bet, right_way, rollCount, print_results):
        self.x = LineBet(min_bet, right_way, rollCount, print_results)
        self.line_bets.append(self.x)




    def shooter_rolls(self):
        while True:
            self.die1 = random.randint(1, 6)
            self.die2 = random.randint(1, 6)
            self.dice = self.die1 + self.die2
            if self.print_results:
                print("You roll a", self.die1, "and", self.die2, "for a total of", self.dice)
            if self.rollCount == 0:
                if self.dice in [7,11]:
                    if self.print_results:
                        print("Pass line wins. Don't pass line loses.")
                    break
                elif self.dice in [2,3,12]:
                    if self.print_results:
                        print("Pass line loses. Don't pass line wins.")
                    break
                else:
                    self.point = self.dice
                    self.rollCount += 1
                    if self.print_results:
                        print("Point =", self.point, "on roll", self.rollCount)
            else:
                if self.dice == self.point:
                    self.rollCount = 0
                    if self.print_results:
                        print("Pass line wins. Don't pass line loses.")
                    break
                elif self.dice == 7:
                    self.rollCount = 0
                    if self.print_results:
                        print("Pass line loses. Don't pass line wins.")
                    break
                else:
                    self.rollCount += 1
                    if self.print_results:
                        print("Point =", self.point, "on roll", self.rollCount)



class LineBet(object):
    def __init__(self, min_bet, right_way, rollCount, print_results):
        """Passed variables"""
        self.min_bet = min_bet
        self.right_way = right_way # Pass/Come (True) bet or Don't Pass/Don't Come (False) bet
        self.rollCount = rollCount
        self.print_results = print_results # True/False whether to print roll by roll stats (for testing)
        """Object tracking variables"""
        self.point = 0
        self.odds_bet = 0
        if self.print_results:
            if self.rollCount == 0:
                if self.right_way:
                    print("Pass bet =", self.min_bet)
                else:
                    print("Don't pass bet =", self.min_bet)
            else:
                if self.right_way:
                    print("Come bet =", self.min_bet)
                else:
                    print("Don't come bet =", self.min_bet)
