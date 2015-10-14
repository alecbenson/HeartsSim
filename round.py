# -*- coding: utf-8 -*-
import trick

class Round:

    def __init__(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count = 0

    def newRound(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count += 1

    def breakHearts(self):
        self.heartsBroken = True

    def update(self, chosenCard):
        # Break hearts if the heart is a legal move and hearts is not broken
        if chosenCard.suit == "♥" and self.heartsBroken == False:
            self.breakHearts()
        # When update is called, we know the first trick is over
        self.firstTrick = False

    def playTricks(self, players):
        # There are 13 tricks in a hand
        for i in range(13):
            current_trick = trick.Trick(players, self)
            current_trick.take_turns()

            players = current_trick.orderPlayers(players)
            print current_trick
