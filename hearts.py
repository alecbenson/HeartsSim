try:
    from cards import Deck, Card
except ImportError:
    pass
import player

class HeartsGame:
    '''A class used to manage the players, cards, and points within the game'''
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.numHumanPlayers = 0
        self.maxPlayers = 4
        self.round = 0
        self.maxPoints = 100

        #Start the game
        self.__play()

    def __play(self):
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
            while(True):
                playerName = raw_input("Enter a name for player {0}: ".format(index))
                if(not playerName.isalnum()):
                    print("Only alphanumeric characters are allowed. Please enter another name.")
                    continue
                self.__addPlayer(playerName, True)
                break

    def __addBotPlayers(self):
        '''Adds additional bot players into the game'''
        if self.numHumanPlayers >= self.maxPlayers:
            return

        botsToAdd = self.maxPlayers - self.numHumanPlayers
        for index in range(botsToAdd):
            botName = "Bot_#{0}".format(index)
            self.__addPlayer(botName, False)

    def __addPlayer(self, name, isHuman):
        '''A helper function used to add a bot or human player to the list of players'''
        newPlayer = player.Player(name, isHuman)

        #The following logic will suffix names with _#X if the name is already in use
        count = 0
        while newPlayer.name in (otherPlayer.name for otherPlayer in self.players):
            count += 1
            newPlayer.name = "{0}_#{1}".format(name,count)
        if count != 0:
            print "The name '{0}' has already been taken, so you will be" \
            "known as '{1}' instead".format(name, newPlayer.name)

        self.players.append(newPlayer)
        print "{0} joined the game.".format(newPlayer.name)

    def __startGame(self):
        '''Starts the turn cycle'''
        while True:
            for player in self.players:
                print "It is now {0}'s turn.".format(player)

    def __queryCardToPlay(self):
        '''Asks the player which card they would like to play during their turn'''


if __name__ == '__main__':
    game = HeartsGame()
