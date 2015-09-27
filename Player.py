"""
Player object holds the information about the player, such as number of units controlled,
territories owned, turn status, etc.
"""

__author__ = 'Isaac'

class Player:
    idCounter = 0

    def __init__(self, name):
        self.name = name
        self.numOfUnits = 15
        self.numOfTerritories = 5
        self.id = self.idCounter
        self.idCounter += 1

    def display(self):
        print(self.name)
