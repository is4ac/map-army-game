"""
Player object holds the information about the player, such as number of units controlled,
territories owned, turn status, etc.
"""

__author__ = 'isung'

class Player:
    def __init__(self, name):
        self.name = name
        self.numOfUnits = 15
        self.numOfTerritories = 5

