# -*- coding: utf-8 -*-

import player
import random
import card
import deck
import hand
import round
import trick


class HeartsGame:
    '''A class used to manage the players, cards, and points within the game'''

    def __init__(self):
        self.deck = deck.Deck()
        self.players = []
        self.numHumanPlayers = 0
        self.maxPlayers = 4
        self.round = round.Round()
        self.maxPoints = 100
        self.discard_pile = hand.Hand()

        # Start the game
        self._play()

    def _play(self):
        '''Used to start the game of hearts'''
        self._initGame()
        self._startGame()

    def _isGameOver(self):
        for player in self.players:
            if player.score >= self.maxPoints:
                return True
        return False

    def _initGame(self):
        '''Invite players and start the game'''
        try:
            playerInput = raw_input("How many human players? ")
            numHumanPlayers = int(playerInput)
            if numHumanPlayers > self.maxPlayers or numHumanPlayers < 0:
                raise ValueError("Hearts requires between 0 and 4 players")
        except ValueError as err:
            print str(err)
            return self._initGame()
        self.numHumanPlayers = numHumanPlayers
        self._addHumanPlayers()
        self._addBotPlayers()

    def _startGame(self):
        '''Starts the turn cycle'''
        while self._isGameOver() == False:
            self.deck = deck.Deck()
            self.deck.dealHands(self.players)
            self.round.newRound()
            self.round.playTricks(self.players)
            self._score_card()

    def _score_card(self):
        ''' Prints a nice, readable scorecard '''
        max_name_len = max([len(player.name) for player in self.players]) + 5
        table_row = "+" + (max_name_len * "-") + "+"
        print table_row
        for player in self.players:
            print "{0}: {1}".format(player.name, player.score)
            print table_row

    def _playerCount(self):
        '''Returns an integer representing the number of players in the game'''
        return len(players)

    def _addHumanPlayers(self):
        '''Adds each human player into the game'''
        for index in range(self.numHumanPlayers):
            playerName = raw_input(
                "Enter a name for player {0}: ".format(index))
            newPlayer = player.Human(playerName)
            self._addPlayer(newPlayer)

    def _addBotPlayers(self):
        '''Adds additional bot players into the game'''
        if self.numHumanPlayers >= self.maxPlayers:
            return
        botsToAdd = self.maxPlayers - self.numHumanPlayers
        for index in range(botsToAdd):
            newBot = player.Bot("Bot", 1)
            self._addPlayer(newBot)

    def _addPlayer(self, player):
        '''A helper function used to add a bot or human player to the list of players'''
        count = 0
        startName = player.name
        while player.name in (otherPlayer.name for otherPlayer in self.players):
            count += 1
            player.name = "{0}_#{1}".format(startName, count)

        print "{0} joined the game.".format(player.name)
        self.players.append(player)

if __name__ == '__main__':
    game = HeartsGame()
