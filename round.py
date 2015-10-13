class round:
    def __init__(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count = 0

    def newRound(self):
        self.heartsBroken = False
        self.firstTrick = True
        self.count += 1

    def breakHearts(self):
        self.heartsBroken = True
