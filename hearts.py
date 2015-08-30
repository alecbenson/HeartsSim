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
        self.numHumanPlayers = 0
        self.maxPlayers = 4
        self.round = 0
        self.maxPoints = 100

        self.__initGame()
        self.__startGame()

    def __playerCount(self):
        '''Returns an integer representing the number of players in the game'''
        return len(players)

    def __initGame(self):
        '''Invite players and start the game'''
        try:
            playerInput = raw_input("How many human players? ")
            numHumanPlayers = int(playerInput)
            if numHumanPlayers > self.maxPlayers or numHumanPlayers < 1:
                raise ValueError("Hearts requires between 1 and 4 players")
        except ValueError as err:
            print str(err)
            return self.__initGame()
        self.numHumanPlayers = numHumanPlayers
        self.__addHumanPlayers()
        self.__addBotPlayers()

    def __addHumanPlayers(self):
        '''Adds each human player into the game'''
        for index in range(self.numHumanPlayers):
            playerName = raw_input("Enter a name for player {0}: ".format(index))
            self.__addPlayer(playerName, True)

    def __addBotPlayers(self):
        '''Adds additional bot players into the game'''
        if self.numHumanPlayers >= self.maxPlayers:
            return

        botsToAdd = self.maxPlayers - self.numHumanPlayers
        for index in range(botsToAdd):
            botName = "Bot_#{0}".format(index)
            print "Adding {0} to the game.".format(botName)
            self.__addPlayer(botName, False)

    def __addPlayer(self, name, isHuman):
        '''A helper function used to add a bot or human player to the list of players'''
        newPlayer = player.Player(name, isHuman)
        self.players.append(newPlayer)

    def __startGame(self):
        '''Starts the turn cycle'''
        while True:
            for player in self.players:
                print "It is now {0}'s turn.".format(player)

    def __queryCardToPlay(self):
        '''Asks the player which card they would like to play during their turn'''


if __name__ == '__main__':
    game = HeartsGame()
