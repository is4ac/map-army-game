"""
Units are the basic fighting unit in the game. They have several attributes such as unit type,
location on grid, health, etc.
"""

__author__ = 'isung'

class Unit:
    def __init__(self, type, x, y, color):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.hp = 10
        self.buff = None

    def attack(self, other, myTerrain, theirTerrain):

