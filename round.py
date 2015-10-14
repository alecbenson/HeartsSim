# -*- coding: utf-8 -*-
import trick
import deck

class Round:

    def __init__(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count = 0
        self.discard_pile = []
        self.cards_in_play = deck.Deck()

    def newRound(self):
        self.cards_in_play = deck.Deck()
        self.discard_pile = []
        self.heartsBroken = False
        self.firstTrick = True
        self.count += 1

    def cards_of_suit_left(self, suit):
        ''' Returns the number of cards still in play with the given suit '''
        count = 0
        for card in self.cards_in_play:
            if card.suit == suit:
                count += 1
        return count

    def breakHearts(self):
        self.heartsBroken = True

    def update(self, chosenCard):
        # Break hearts if the heart is a legal move and hearts is not broken
        if chosenCard.suit == "♥" and self.heartsBroken == False:
            self.breakHearts()
        # When update is called, we know the first trick is over
        self.firstTrick = False

        #Add to the discard and cards in play pile
        self.discard_pile.append(chosenCard)
        self.cards_in_play.remove(chosenCard)

    def playTricks(self, players, firstPlayer):
        # Set initial turn order
        current_trick = trick.Trick(players, self)
        players = current_trick.orderPlayers(players, firstPlayer)

        # There are 13 tricks in a hand
        for i in range(13):
            current_trick = trick.Trick(players, self)
            current_trick.take_turns()

            players = current_trick.orderPlayers(players)
            print current_trick
