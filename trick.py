# -*- coding: utf-8 -*-


class Trick:
    ''' The trick class is used to represent a single set of four turns within a game '''

    def __init__(self, players, round):
        self.start_card = None
        self.round = round

        self.players = players
        self.played_cards = {}

    def take_turns(self):

        prompt = "It is your turn -- choose a card to play: "
        for player in self.players:
            chosenCard = player.queryCardToPlay(prompt, self.round, self)

            # Repeat until the player makes a legal move
            while not self.isLegalMove(player, chosenCard):
                illegal_prompt = "That's not a legal move. Try again: "
                chosenCard = player.queryCardToPlay(
                    illegal_prompt, self.round, self)

            self._confirm_move(player, chosenCard)

    def _confirm_move(self, player, chosenCard):
        '''
        A helper function to update the status of the trick after
        a player makes a turn
        '''
        player.hand.play_card(chosenCard)
        self.played_cards[player] = chosenCard
        # Inform the round if hearts were broken or that the first trick is
        # over
        self.round.update(chosenCard)
        # Update the start card of the trick if necessary
        if self.start_card == None:
            self.start_card = chosenCard
        # Inform players that a move has been made
        print "{0} played:\n{1}".format(player.name, chosenCard)

    def score(self):
        ''' Returns the player that won the trick and awards them points '''
        if not self.played_cards:
            print "The trick is empty, there can be no winner."
            return None

        winning_player = None
        winning_card = self.start_card
        trick_points = self.value()

        for player, card in self.played_cards.iteritems():
            if card.suit == self.start_card.suit:
                if card.getWeight() >= winning_card.getWeight():
                    winning_player = player
                    winning_card = card

        winning_player.addPoints(trick_points)
        self._trick_summary(winning_player, trick_points)

        return winning_player

    def value(self):
        trick_points = 0
        for player, card in self.played_cards.iteritems():
            trick_points += card._getPoints()
        return trick_points

    def _trick_summary(self, winning_player, trick_points):
        ''' Prints a quick summary of the hand '''
        print "The trick is over. {0} won the trick, and received {1} points." \
            .format(winning_player.name, trick_points)

    def moves_left(self):
        return 4 - len(self.played_cards)

    def current_winning_card(self):
        if self.start_card == None:
            return None
        current_winner = self.start_card
        for player, card in self.played_cards.iteritems():
            if card.suit == current_winner.suit:
                if card.getWeight > current_winner.getWeight:
                    current_winner = card
        return current_winner

    def card_list(self):
        ''' Returns the cards in the trick as a list '''
        return self.played_cards.values()

    def __str__(self):
        zipped = zip(*[card.templatedParts()
                       for card in self.played_cards.values()])
        result = "\n".join("".join(map(str, l)) for l in zipped)
        return result

    def orderPlayers(self, players, startPlayer=None):
        order = []
        if startPlayer == None:
            startPlayer = self.score()
        nextStartPlayer = players.index(startPlayer)
        for i in range(len(players)):
            order.append(players[(nextStartPlayer + i) % 4])
        return order

    def isLegalMove(self, player, chosenCard):
        if self.start_card is None:
            if self.round.firstTrick:
                return True  # TODO: change to only return True on 2 of clubs
            if self.round.heartsBroken:
                return True
            elif chosenCard.suit != '♥':
                return True
            elif player.hand.onlyHeartsLeft():
                return True
            return False
        if self.round.firstTrick:
            if chosenCard.suit == '♣':
                return True
            if not player.hand.hasSuit('♣'):
                if (chosenCard.suit != '♥') or not (chosenCard.suit == '♠' and chosenCard.value == 'Q'):
                    return True
                return False
        if chosenCard.suit == self.start_card.suit:
            return True
        if not player.hand.hasSuit(self.start_card.suit):
            return True
        return False
