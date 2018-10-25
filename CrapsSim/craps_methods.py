import random

class CrapsGame(object):
    def __init__(self, min_bet, start_amount, working, print_results):
        """Passed variables"""
        self.min_bet = min_bet  # amount bet (int) on pass/don't pass line, come/don't come line
        self.start_amount = start_amount  # $ amount with which one walks up to table
        self.pot_amount = start_amount  # track $$ left in pot after each shooter roll
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
        if self.pot_amount >= bet:
            self.x = Bet(type, bet, right_way, self.print_results)
            self.bets.append(self.x)
            self.pot_amount -= bet
            if self.print_results:
                print("Pot amount =", self.pot_amount)

    def set_point(self, type, point):
        for x in self.bets:
            if x.type == "Pass":
                x.point = point

    def set_odds(self, type, bet, point, right_way):
        for x in self.bets:
            if (x.type == "Pass") and (x.right_way == right_way) and (x.point == point):
                change = bet - x.odds_bet
                if change != 0 and self.pot_amount >= change:
                    x.odds_bet = bet
                    self.pot_amount -= change
                    if self.print_results:
                        if x.right_way:
                            print(x.type, "Odds bet =", change, "Pot amount =", self.pot_amount)
                        else:
                            print("Don't", x.type, "Odds bet =", change, "Pot amount =", self.pot_amount)

    def pay_bet(self, type, win):
        winnings = 0
        for x in self.bets:
            if type == "Field" and type == x.type:
                if win:
                    winnings += 2 * x.bet
                    if self.dice == 2:
                        winnings += x.bet
                    elif self.dice == 12:
                        winnings += 2 * x.bet
                self.bets.remove(x)
            if type == "Pass" and type == x.type:
                if (win and x.right_way):
                    winnings += 2 * x.bet
                    if x.point in [4,10]:
                        winnings += x.odds_bet + x.odds_bet * 2
                    elif x.point in [5,9]:
                        winnings += x.odds_bet + x.odds_bet * 3 / 2
                    elif x.point in [6,8]:
                        winnings += x.odds_bet + x.odds_bet * 6 / 5
                elif (not win and not x.right_way):
                    if self.rollCount == 0 and self.dice == 12:
                        winnings = x.bet # Push for 12 on Don't pass comeout roll
                    else:
                        winnings += 2 * x.bet
                        if x.point in [4,10]:
                            winnings += x.odds_bet + x.odds_bet / 2
                        elif x.point in [5,9]:
                            winnings += x.odds_bet + x.odds_bet * 2 / 3
                        elif x.point in [6,8]:
                            winnings += x.odds_bet + x.odds_bet * 5 / 6
                self.bets.remove(x)
        winnings = int(winnings)
        self.pot_amount += winnings
        if self.print_results:
            print("Winnings =", winnings, "Pot amount =", self.pot_amount)


    def shooter_rolls(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.dice = self.die1 + self.die2
        if self.print_results:
            print("You roll a", self.die1, "and", self.die2, "for a total of", self.dice)
        if self.dice in [2,3,4,9,10,11,12]: # Field Bet
            if self.print_results:
                print("Field bet wins.")
            self.pay_bet("Field", True)
        else:
            if self.print_results:
                print("Field bet loses.")
            self.pay_bet("Field", False)
        if self.rollCount == 0: # Comeout roll
            if self.dice in [7,11]:
                if self.print_results:
                    print("Pass line wins. Don't pass line loses.")
                self.pay_bet("Pass", True)
                self.resolved = True
            elif self.dice in [2,3,12]:
                if self.print_results:
                    print("Pass line loses. Don't pass line wins/pushes.")
                self.pay_bet("Pass", False)
                self.resolved = True
            else:
                self.point = self.dice
                self.rollCount += 1
                self.set_point("Pass", self.point)
                if self.print_results:
                    print("Point =", self.point, "on roll", self.rollCount)
        else: # Point roll
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
