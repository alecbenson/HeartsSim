class Trick:
    ''' The trick class is used to represent a single set of four turns within a game '''
    def __init__(self):
        self.played_cards = {}
        self.start_card = None

    def add(self, player, card):
        ''' Keys a player in the trick with the card that they played '''
        if self.start_card == None:
            self.start_card = card
        self.played_cards[player] = card

    def score(self):
        ''' Returns the player that won the trick '''
        if not self.played_cards:
            print "The trick is empty, there can be no winner."
            return None

        winning_player = None
        winning_card = self.start_card
        trick_points = 0

        for player, card in self.played_cards.iteritems():
            trick_points += card._getPoints()
            if card.suit == self.start_card.suit:
                if card.getWeight() >= winning_card.getWeight():
                    winning_player = player
                    winning_card = card

        winning_player.addPoints(trick_points)
        self._trick_summary(winning_player, trick_points)
        return winning_player

    def _trick_summary(self, winning_player, trick_points):
        ''' Prints a quick summary of the hand '''
        print "The trick is over. {0} won the trick, and received {1} points." \
            .format(winning_player.name, trick_points)

    def card_list(self):
        ''' Returns the cards in the trick as a list '''
        return self.played_cards.values()

    def __str__(self):
        zipped = zip(*[card.templatedParts() for card in self.played_cards.values()])
        result = "\n".join("".join(map(str,l)) for l in zipped)
        return result
