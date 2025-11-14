from random import randint
import random
class Character:
    def __init__(self, name, hp, xp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.xp = xp
        self.level = 1
        self.gold = 0
        self.level_ups_list = [0, 10, 20, 30, 40, 50]
        self.alive = True

    def take_damage(self, amount, attacker, logs):
        log = [("You: Hit for ", "normal"), (f"-{amount}", "damage"), (" HP", "hp_value")]
        logs.add_line(log)

        self.hp = self.hp - amount

        if(self.hp <= 0):
            self.hp = 0
            if (attacker != None):
                self.gain_xp(attacker)
            self.alive = False


    def show_hp(self):
        return self.hp

    def gain_xp(self, attacker):
        attacker.xp = attacker.xp + self.xp
        attacker.level_up()

    def show_xp(self):
        return self.xp


class Player(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attack(self):
        return randint(1, 3 + self.level *2)

    def level_up(self):
        if(self.xp >= self.level_ups_list[self.level]):
            self.xp = self.xp - self.level_ups_list[self.level]
            self.level = self.level + 1
            self.level_up()



class Monster(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def flee(self, player):
        flee_chance = 1 - pow(0.5, (player.level - self.level + 1))
        if flee_chance < 0:
            flee_chance = 0
        print(f"Chance to flee is: {flee_chance * 100}%.")
        if (random.random() <= flee_chance):
            return 1
        else:
            return 0




