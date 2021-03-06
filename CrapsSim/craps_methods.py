import random

class CrapsGame(object):
    def __init__(self, min_bet, start_amount, working, print_results):
        """Passed variables"""
        self.min_bet = min_bet  # amount bet (int) on pass/don't pass line, come/don't come line
        self.pot_amount = start_amount  # track $$ left in pot after each shooter roll
        self.working = working  # track whether or not to let Come Odds "work" on the Come Out roll (Don't Come Odds always ON)
        self.print_results = print_results # True/False whether to print roll by roll stats (for testing)
        """Object tracking variables"""
        self.total_bet = 0 # track $$ bet
        self.total_won = 0 # track $$ won
        self.total_lost = 0 # track $$ lost
        self.bets = []  # list of Bet objects to track
        self.die1 = 0
        self.die2 = 0
        self.dice = 0
        self.rollCount = 0
        self.point = 0
        self.resolved = False

    def add_bet(self, type, bet, right_way): # Types are: Pass, Field, Place4, Place5, Place6, Place8, Place9, Place10
        if type in ["Pass", "Field"]:
            if self.pot_amount >= bet:
                x = Bet(type, bet, right_way, self.print_results)
                self.bets.append(x)
                self.pot_amount -= bet
                self.total_bet += bet
                if self.print_results:
                    print("Pot amount =", self.pot_amount)
        if type in ["Place4", "Place5", "Place6", "Place8", "Place9", "Place10"]:
            existing_bet = False
            for x in self.bets:
                #print(x.type, "bet =", x.bet, ", point =", x.point, ", odds bet =", x.odds_bet)
                if type == x.type:
                    existing_bet = True
                    change = bet - x.bet
                    if change != 0 and self.pot_amount >= change:
                        x.bet = bet
                        self.pot_amount -= change
                        self.total_bet += change
                        if bet == 0:
                            self.bets.remove(x)
                        if self.print_results:
                            if bet == 0:
                                print(type, "Bet taken down. Pot amount =", self.pot_amount)
                            else:
                                print(type, "Bet =", bet, "Pot amount =", self.pot_amount)
            else:
                if not existing_bet:
                    if self.pot_amount >= bet and bet != 0:
                        x = Bet(type, bet, right_way, self.print_results)
                        self.bets.append(x)
                        self.pot_amount -= bet
                        self.total_bet += bet
                        if self.print_results:
                            print("Pot amount =", self.pot_amount)

    def _set_point(self, type, point):
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
                    self.total_bet += change
                    if self.print_results:
                        if x.right_way:
                            print(x.type, "Odds bet =", change, "Pot amount =", self.pot_amount)
                        else:
                            print("Don't", x.type, "Odds bet =", change, "Pot amount =", self.pot_amount)

    def pay_bet(self, type, won_bet):
        bet = 0
        won = 0
        lost = 0
        for x in self.bets:

            if type == "Field" and type == x.type:
                if won_bet:
                    bet += x.bet
                    won += x.bet
                    if self.dice == 2:
                        won += x.bet # Field 2 pays double
                    if self.dice == 12:
                        won += 2 * x.bet # Field 12 pays triple
                    if self.print_results:
                        print("Field bet wins.")
                else:
                    lost += x.bet
                    if self.print_results:
                        print("Field bet loses.")
                self.bets.remove(x)

            if type == "Pass" and type == x.type:
                if x.right_way:
                    if won_bet:
                        bet += x.bet + x.odds_bet
                        won += x.bet
                        if x.point in [4,10]:
                            won += x.odds_bet * 2
                        if x.point in [5,9]:
                            won += x.odds_bet * 3 / 2
                        if x.point in [6,8]:
                            won += x.odds_bet * 6 / 5
                        if self.print_results:
                            print("Pass line wins.")
                    else:
                        lost += x.bet + x.odds_bet
                        if self.print_results:
                            print("Pass line loses.")
                else:
                    if not won_bet:
                        if self.rollCount == 0 and self.dice == 12:
                            bet += x.bet # Push for 12 on Don't pass comeout roll
                        else:
                            bet += x.bet + x.odds_bet
                            won += x.bet
                            if x.point in [4,10]:
                                won += x.odds_bet / 2
                            if x.point in [5,9]:
                                won += x.odds_bet * 2 / 3
                            if x.point in [6,8]:
                                won += x.odds_bet * 5 / 6
                            if self.print_results:
                                print("Don't pass line wins/pushes.")
                    else:
                        lost += x.bet + x.odds_bet
                        if self.print_results:
                            print("Don't pass line loses.")
                self.bets.remove(x)

            if type in ["Place4", "Place5", "Place6", "Place8", "Place9", "Place10"] and type == x.type:
                if not won_bet:
                    lost += x.bet
                    if self.print_results:
                        print(type, "loses.")
                else:
                    if type in ["Place4", "Place10"]:
                        bet += x.bet
                        won += x.bet * 9 / 5
                    if type in ["Place5", "Place9"]:
                        bet += x.bet
                        won += x.bet * 7 / 5
                    if type in ["Place6", "Place8"]:
                        bet += x.bet
                        won += x.bet * 7 / 6
                    if self.print_results:
                        print(type, "wins.")
                self.bets.remove(x)

        winnings = int(won)
        self.pot_amount += winnings + bet
        self.total_won += winnings
        self.total_lost += lost
        if self.print_results and bet != 0:
            print("Bets =", bet, "Won =", winnings, "Lost =", lost, "Pot amount =", self.pot_amount)


    def shooter_rolls(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.dice = self.die1 + self.die2
        if self.print_results:
            print("You roll a", self.die1, "and", self.die2, "for a total of", self.dice)

        if self.dice in [2,3,4,9,10,11,12]: # Field Bet
            self.pay_bet("Field", True) # Wins
        else:
            self.pay_bet("Field", False) # Loses

        if self.rollCount == 0: # Comeout roll, place bets off
            if self.dice in [2,3,7,11,12]:
                self.resolved = True
                if self.dice in [7,11]:
                    self.pay_bet("Pass", True)
                else:
                    self.pay_bet("Pass", False)
            else:
                self.point = self.dice
                self.rollCount += 1
                self._set_point("Pass", self.point)
                if self.print_results:
                    print("Point =", self.point, "on roll", self.rollCount)
        else: # Point roll
            if self.dice == 4:
                self.pay_bet("Place4", True)
            if self.dice == 5:
                self.pay_bet("Place5", True)
            if self.dice == 6:
                self.pay_bet("Place6", True)
            if self.dice == 8:
                self.pay_bet("Place8", True)
            if self.dice == 9:
                self.pay_bet("Place9", True)
            if self.dice == 10:
                self.pay_bet("Place10", True)
            if self.dice == 7:
                self.pay_bet("Pass", False)
                self.pay_bet("Place4", False)
                self.pay_bet("Place5", False)
                self.pay_bet("Place6", False)
                self.pay_bet("Place8", False)
                self.pay_bet("Place9", False)
                self.pay_bet("Place10", False)
                self.resolved = True
            if self.dice == self.point:
                self.pay_bet("Pass", True)
                self.resolved = True
            if self.resolved:
                self.rollCount = 0
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
