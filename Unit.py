"""
Units are the basic fighting unit in the game. They have several attributes such as unit type,
location on grid, health, etc.
"""

__author__ = 'Isaac'

import math

class Unit:
    def __init__(self, type, x, y, color, group, owner):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.hp = 10
        self.buff = None
        self.att = 1
        self.group = group
        self.range = 1
        self.owner = owner
        self.char = " "
        self.moveRange = 5
        self.moveQueue = []

        # set attack value based on type
        self.initialize()

    # Initializes attack and range values based on what type you are
    def initialize(self):
        if self.type == "infantry":
            self.att = 2
            self.char = "I"
        elif self.type == "cavalry":
            self.att = 2
            self.char = "C"
            self.moveRange += 2
        elif self.type == "archer":
            self.att = 2
            self.range = 2
            self.char = "A"
        elif self.type == "pikeman":
            self.att = 1
            self.char = "P"
        elif self.type == "hoplite":
            self.att = 1
            self.range = 2
            self.char = "H"

    # Full battle sequence, I attack first, other attacks back
    def battle(self, other, myTerrain, theirTerrain):
        # check to see if other unit is attack-able
        if other.owner != self.owner:
            alive = self.deal_damage(other, theirTerrain)

            if alive:
                other.deal_damage(self, myTerrain)

    # Do one round of attacks, I hit the other guy and if he dies,
    # I return False, if he survives, I return True
    def deal_damage(self, other, theirTerrain):
        calcAtt = self.att

        # check strengths/weaknesses
        if self.type == "infantry" and other.type == "cavalry":
            # weakened damage output
            calcAtt -= 0.5
        elif self.type == "cavalry":
            if other.type == "archer" or other.type == "infantry":
                # strong damage output
                calcAtt += 1
            elif other.type == "pikeman":
                # weakened damage output
                calcAtt -= 0.5
        elif self.type == "archer":
            if other.type == "infantry" or other.type == "pikeman":
                # strong damage output
                calcAtt += 0.5
            elif other.type == "hoplite":
                # weakened damage output
                calcAtt -= 1
        elif self.type == "pikeman":
            if other.type == "cavalry":
                # strong damage output
                calcAtt += 2
        elif self.type == "hoplite":
            if other.type == "archer":
                # strong damage output
                calcAtt += 2

        # Dish out the DAMAGE!!!! #getwrecked
        damage = math.floor((self.hp/5)*calcAtt - theirTerrain.defense)
        other.hp -= damage

        if other.hp <= 0:
            other.hp = 0
            return False
        else:
            return True

    # add to move queue if within range
    def addMove(self, dire):
        if len(self.moveQueue) < self.range:
            self.moveQueue.append(dire)
        else:
            self.moveQueue.append(None)  # indicates movement beyond range

    # cloning function
    def clone(self):
        newUnit = Unit(self.type, self.x, self.y, self.color, self.group, self.owner)
        newUnit.hp = self.hp
        return newUnit

    # Debugging purposes
    def display(self):
        print(self.type + ":")
        print("HP: " + str(self.hp))