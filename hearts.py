try:
    from cards import Deck, Card
except ImportError:
    pass
import player
import sys

class HeartsGame:
    '''A class used to manage the players, cards, and points within the game'''
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.numPlayers = 0
        self.__initGame()

    def __playerCount(self):
        '''Returns an integer representing the number of players in the game'''
        return len(players)

    def __initGame(self):
        '''Invite players and start the game'''
        try:
            playerInput = raw_input("How many human players? ")
            numPlayers = int(playerInput)
            if numPlayers > 4 or numPlayers < 1:
                raise ValueError("Hearts requires between 1 and 4 players")
        except ValueError as err:
            print str(err)
            self.__initGame()
        self.numPlayers = numPlayers
        self.__addPlayers()

    def __addPlayers(self):
        '''Adds each player into the game'''
        playerIndex = 1
        while len(self.players) < self.numPlayers:
            playerName = raw_input("Enter a name for player {0}: ".format(playerIndex))
            playerIndex += 1
            newPlayer = player.Player(playerName, None)
            self.players.append(newPlayer)
