from random import randint
class Character:
    def __init__(self, name, hp, xp):
        self.name = name
        self.hp = hp
        self.xp = xp
        self.level = 1
        self.level_ups_list = [0, 10, 20, 30, 40, 50]
        self.alive = True



    def take_damage(self, amount, attacker=None):
        self.hp = self.hp - amount
        if(self.hp <= 0):
            self.hp = 0
            if (attacker != None):
                self.gain_xp(attacker)
            self.alive = False



    def attack(self):
        return randint(1, 3 + self.level *2)

    def show_hp(self):
        return self.hp

    def gain_xp(self, attacker):
        attacker.xp = attacker.xp + self.xp
        attacker.level_up()

    def show_xp(self):
        return self.xp

    def level_up(self):
        if(self.xp >= self.level_ups_list[self.level]):
            self.xp = self.xp - self.level_ups_list[self.level]
            self.level = self.level + 1
            print(self.name + " just leveled up to level " + str(self.level))




