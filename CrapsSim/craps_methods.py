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
        self.bets = []  # list of Bet objects to track
        self.die1 = 0
        self.die2 = 0
        self.dice = 0
        self.rollCount = 0
        self.point = 0
        self.resolved = False

    def add_bet(self, type, bet, right_way):
        self.x = Bet(type, bet, right_way, self.print_results)
        self.bets.append(self.x)
        self.pot_amount -= bet
        if self.print_results:
            print("Pot amount =", self.pot_amount)

    def pay_bet(self, type, win):
        winnings = 0
        for x in self.bets:
            if x.type == "Pass":
                if (win and x.right_way) or (not win and not x.right_way):
                    winnings += 2 * x.bet
                self.bets.remove(x)
        self.pot_amount += winnings
        if self.print_results:
            print("Winnings =", winnings, "Pot amount =", self.pot_amount)


    def shooter_rolls(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.dice = self.die1 + self.die2
        if self.print_results:
            print("You roll a", self.die1, "and", self.die2, "for a total of", self.dice)
        if self.rollCount == 0:
            if self.dice in [7,11]:
                if self.print_results:
                    print("Pass line wins. Don't pass line loses.")
                self.pay_bet("Pass", True)
                self.resolved = True
            elif self.dice in [2,3,12]:
                if self.print_results:
                    print("Pass line loses. Don't pass line wins.")
                self.pay_bet("Pass", False)
                self.resolved = True
            else:
                self.point = self.dice
                self.rollCount += 1
                if self.print_results:
                    print("Point =", self.point, "on roll", self.rollCount)
        else:
            if self.dice == self.point:
                if self.print_results:
                    print("Pass line wins. Don't pass line loses.")
                self.pay_bet("Pass", True)
                self.resolved = True
            elif self.dice == 7:
                if self.print_results:
                    print("Pass line loses. Don't pass line wins.")
                self.pay_bet("Pass", False)
                self.resolved = True
            else:
                self.rollCount += 1
                if self.print_results:
                    print("Point =", self.point, "on roll", self.rollCount)



class Bet(object):
    def __init__(self, type, bet, right_way, print_results):
        """Passed variables: type, bet, True/False (Pass/Don't pass), True/False (Print/Don't print)"""
        self.type = type
        self.bet = bet
        self.right_way = right_way # Pass/Come (True) bet or Don't Pass/Don't Come (False) bet
        self.print_results = print_results # True/False whether to print roll by roll stats (for testing)
        """Object tracking variables"""
        self.point = 0
        self.odds_bet = 0
        if self.print_results:
            if self.right_way:
                print(self.type, "bet =", self.bet)
            else:
                print("Don't", self.type, "bet =", self.bet)
