import abc
import typing


class Card:
    def __init__(self):
        return

    def cost(self):
        return


class Player:
    def __init__(self):
        hand: typing.List[Card] = []
        return


class Battlefield:
    def __init__(self):
        self.players: typing.List[Player] = []
        return
