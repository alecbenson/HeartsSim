# -*- coding: utf-8 -*-
import trick
import deck
import card


class Round:

    def __init__(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count = 0
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

    def _findTwo(self, players):
        for player in players:
            if card.Card('♣', '2') in player.hand:
                return player

    def update(self, chosenCard):
        # Break hearts if card is worth points and hearts is not broken
        if chosenCard._getPoints() > 0 and self.heartsBroken == False:
            self.breakHearts()
        # When update is called, we know the first trick is over
        self.firstTrick = False

        # Add to the discard and cards in play pile
        self.cards_in_play.remove(chosenCard)

    def new_trick_text(self):
        bold = '\033[1m'
        underline = '\033[4m'
        dashes = "\t" * 3
        text = "New Trick"
        reset = '\033[0m'
        print "{0}{1}{2}{3}{2}{4}".format(bold, underline, dashes, text, reset)

    def playTricks(self, players):
        # Set initial turn order
        current_trick = trick.Trick(players, self)
        self.passCards(players)

        startPlayer = self._findTwo(players)
        players = current_trick.orderPlayers(players, startPlayer)

        # There are 13 tricks in a hand
        for i in range(13):
            self.new_trick_text()
            current_trick = trick.Trick(players, self)
            current_trick.take_turns()

            players = current_trick.orderPlayers(players)
            print current_trick

    def passCards(self, players):
        # If we are not holding cards, return
        if (self.count % 4) == 3:
            return

        # pick 3 cards to give up
        for player in players:
            for i in range(3):
                card_to_pass = player.queryCardToPass()
                player.passedCards.append(card_to_pass)

        for player in players:
            i = players.index(player)
            if (self.count % 4) == 0:  # Passing left
                for card in players[(i + 1) % 4].passedCards:
                    player.hand.add_card(card)
                player.hand.sortCards()

            elif (self.count % 4) == 1:  # Passing right
                for card in players[(i + 3) % 4].passedCards:
                    player.hand.add_card(card)
                player.hand.sortCards()

            elif (self.count % 4) == 2:  # Passing Across
                for card in players[(i + 2) % 4].passedCards:
                    player.hand.add_card(card)
                player.hand.sortCards()

        # Clear the passed cards
        for player in players:
            player.passedCards = []
