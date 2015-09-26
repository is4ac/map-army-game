"""
Units are the basic fighting unit in the game. They have several attributes such as unit type,
location on grid, health, etc.
"""

__author__ = 'isung'

import math

class Unit:
    def __init__(self, type, x, y, color, group):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.hp = 10
        self.buff = None
        self.att = 1
        self.group = group
        self.range = 1

        # set attack value based on type
        self.set_attack_and_range()

    # Initializes attack and range values based on what type you are
    def set_attack_and_range(self):
        if self.type == "infantry":
            self.att = 2
        elif self.type == "cavalry":
            self.att = 2
        elif self.type == "archer":
            self.att = 2
            self.range = 2
        elif self.type == "pikeman":
            self.att = 1
        elif self.type == "hoplite":
            self.att = 1
            self.range = 2

    # Full battle sequence, I attack first, other attacks back
    def battle(self, other, myTerrain, theirTerrain):
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
