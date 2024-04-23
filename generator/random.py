from numpy import random


class CustomRandom():
    def __init__(self):
        self.random_generator = random.default_rng()

    def random(self):
        rnd = self.random_generator.random()
        while rnd == 1:
            rnd = self.random_generator.random()
        return rnd
