import player, card, deck, hand

class HeartsGame:
    '''A class used to manage the players, cards, and points within the game'''
    def __init__(self):
        self.deck = deck.Deck()
        self.players = []
        self.numHumanPlayers = 0
        self.maxPlayers = 4
        self.round = 0
        self.maxPoints = 100
        self.playedCards = hand.Hand()

        #Start the game
        self._play()

    def _play(self):
        '''Used to start the game of hearts'''
        self._initGame()
        self._startGame()

    def _initGame(self):
        '''Invite players and start the game'''
        try:
            playerInput = raw_input("How many human players? ")
            numHumanPlayers = int(playerInput)
            if numHumanPlayers > self.maxPlayers or numHumanPlayers < 1:
                raise ValueError("Hearts requires between 1 and 4 players")
        except ValueError as err:
            print str(err)
            return self._initGame()
        self.numHumanPlayers = numHumanPlayers
        self._addHumanPlayers()
        self._addBotPlayers()

    def _startGame(self):
        '''Starts the turn cycle'''
        self.deck.dealHands(self.players)
        while True:
            #Empty the hand at the beginning of the round
            self.playedCards.empty()
            for player in self.players:
                print "It is now {0}'s turn:\n{1}".format(player, player.hand)
                chosenCard = player.queryCardToPlay()
                self.playedCards.addCard(chosenCard)
                print "The following cards have been played:\n{0}".format(self.playedCards)

    def _playerCount(self):
        '''Returns an integer representing the number of players in the game'''
        return len(players)

    def _addHumanPlayers(self):
        '''Adds each human player into the game'''
        for index in range(self.numHumanPlayers):
            playerName = raw_input("Enter a name for player {0}: ".format(index))
            self._addPlayer(playerName, True)

    def _addBotPlayers(self):
        '''Adds additional bot players into the game'''
        if self.numHumanPlayers >= self.maxPlayers:
            return

        botsToAdd = self.maxPlayers - self.numHumanPlayers
        for index in range(botsToAdd):
            botName = "Bot_#{0}".format(index)
            self._addPlayer(botName, False)

    def _addPlayer(self, name, isHuman):
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

if __name__ == '__main__':
    game = HeartsGame()
