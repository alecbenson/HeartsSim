import player
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
            self.passCards()

            # There are 13 tricks in a hand
            for i in range(13):
                # Empty the hand at the beginning of the round
                current_trick = trick.Trick()
                self.discard_pile.empty()
                for player in self.players:
                    prompt = "It is your turn -- choose a card to play: "
                    chosenCard = player.queryCardToPlay(
                        prompt, self.round, current_trick.start_card)
                    current_trick.add(player, chosenCard)
                # Score the trick
                self.players = current_trick.orderPlayers(self.players)
                print current_trick
                # Add the played cards to the discard pile
                self.discard_pile.addCards(current_trick.card_list())
                self.round.firstTrick = False
            self.round.newRound()
        # Determine Winner
        self._score_card()

    def _playerCount(self):
        '''Returns an integer representing the number of players in the game'''
        return len(players)

    def _score_card(self):
        ''' Prints a nice, readable scorecard '''
        max_name_len = max([len(player.name) for player in self.players]) + 5
        table_row = "+" + (max_name_len * "-") + "+"
        print table_row
        for player in self.players:
            print "{0}: {1}".format(player.name, player.score)
            print table_row

    def _addHumanPlayers(self):
        '''Adds each human player into the game'''
        for index in range(self.numHumanPlayers):
            playerName = raw_input(
                "Enter a name for player {0}: ".format(index))
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

        # The following logic will suffix names with _#X if the name is already
        # in use
        count = 0
        while newPlayer.name in (otherPlayer.name for otherPlayer in self.players):
            count += 1
            newPlayer.name = "{0}_#{1}".format(name, count)
        if count != 0:
            print "The name '{0}' has already been taken, so you will be" \
                "known as '{1}' instead".format(name, newPlayer.name)

        self.players.append(newPlayer)
        print "{0} joined the game.".format(newPlayer.name)

    def passCards(self):
        # If we are not holding cards, return
        round_count = self.round.count
        if (round_count % 4) == 3:
            return

        # pick 3 cards to give up
        for player in self.players:
            for i in range(3):
                player.passedCards.append(player.queryCardToPass())

        for player in self.players:
            i = self.players.index(player)
            if (round_count % 4) == 0:  # Passing left
                for card in self.players[(i + 1) % 4].passedCards:
                    player.hand.addCard(card)
                player.hand.sortCards()

            elif (round_count % 4) == 1:  # Passing right
                for card in self.players[(i + 3) % 4].passedCards:
                    player.hand.addCard(card)
                player.hand.sortCards()

            elif (round_count % 4) == 2:  # Passing Across
                for card in self.players[(i + 2) % 4].passedCards:
                    player.hand.addCard(card)
                player.hand.sortCards()

        # Clear the passed cards
        for player in self.players:
            player.passedCards = []

if __name__ == '__main__':
    game = HeartsGame()
