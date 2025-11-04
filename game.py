import random
from random import randint
import math
class Game:
    def __init__(self, player, location):
        self.player = player
        self.location = location
        self.locations = []
        self.can_flee = True
        self.mode = "EXPLORE"
        self.encounter = None
        self.commands = {
            "EXPLORE" : {
                "M" : self.cmd_move,
                "A" : self.cmd_hunt,

            },
            "ENCOUNTER": {
                "A" : self.cmd_attack,
                "F" : self.cmd_flee,
            }
        }
    def main_game_loop(self):
        while True:
            if self.mode == "EXPLORE":
                prompt = "[M] to move, [A] to hunt"
            else:
                prompt = "[A] to attack, [F] to flee"
            cmd = input(f"{prompt}\n").strip().upper()
            action = self.commands[self.mode][cmd]
            if not action:
                print("Unknown command. Press ? for help.")
                continue
            action()

    def cmd_help(self):
        if(self.mode == "EXPLORE"):
            print(f"{self.location} with enemies: {self.location.print_enemies()}")
        else:
            enemy = self.encounter
            print(f"Combat with {enemy.name} with [{enemy.hp} HP]")

    def cmd_move(self, destination):

        destination_index = self.locations.index(destination)
        try:
            self.location = destination
        except ValueError:
            print(f"Location {destination} not found.")

    def cmd_hunt(self):
        enemies_count = len(self.location.enemies)
        enemy_index = randint(0, enemies_count-1)
        self.encounter = self.location.enemies[enemy_index]
        self.mode = "ENCOUNTER"
        self.cmd_help()

    def cmd_attack(self):
        dmg_amount = self.player.attack()
        self.encounter.take_damage(dmg_amount, self.player)

    def cmd_flee(self):
        if(self.can_flee):
            flee_chance = 1 - pow(0.5,  (self.player.level - self.encounter.level + 1))
            if flee_chance < 0:
                flee_chance = 0
            print(f"Chance to flee is: {flee_chance*100}%.")
            if(random.random() <= flee_chance):
                self.encounter = None
                self.mode = "EXPLORE"
                print(f"Flee was successful")
            else:
                print(f"Flee wasn't successful")
                self.can_flee = False
        else:
            pass





