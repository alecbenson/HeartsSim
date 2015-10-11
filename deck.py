# -*- coding: utf-8 -*-

import card
from random import shuffle

class Deck:
    '''A simple class that represents a standard deck of 52 cards'''
    def __init__(self):
        self.cards = []
        self._newDeck()

    def _newDeck(self):
        '''Instantiate a new, shuffled deck'''
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♥", "♦", "♠", "♣"]
        for value in values:
            for suit in suits:
                new_card = card.Card(suit, value)
                self.cards.append(new_card)
        self.shuffle()

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        '''Shuffle all cards in the deck'''
        shuffle(self.cards)

    def deal(self):
        '''Pull a single card from the deck'''
        return self.cards.pop(0)

    def dealHands(self, players):
        '''Distributes the deck amongst the players'''
        while len(self.cards) != 0:
            for player in players:
                dealtCard = self.deal()
                player.hand.addCard(dealtCard)
