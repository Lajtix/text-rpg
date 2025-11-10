import random
from random import randint
import math
import os
from models.logs import MessageLogs, EncounterLogs
from ui.encounter_view import EncounterView


class GameModel:
    def __init__(self, player, location):
        self.player = player
        self.location = location
        self.locations = []
        #self.message_logs = None
        self.message_logs = self.message_logs = MessageLogs()
        self.can_flee = True
        self.mode = "EXPLORE"
        self.encounter = None
        self.prompt = "[M] to move, [A] to hunt"
       # self.combat_log = []
        self.player_log = []
        self.encounter_log = []

        self.commands = {
            "EXPLORE" : {
                "M" : self.cmd_move,
                "A" : self.cmd_hunt,

            },
            "ENCOUNTER": {
                "A" : self.cmd_attack,
                "F" : self.cmd_flee,
            },
            "ENCOUNTER_END": {
                "L" : self.cmd_leave,
            },
        }
    def run(self, stdscr):
        self.main_game_loop()

    def process_command(self, cmd):
        action = self.commands[self.mode][cmd]
        if not action:
            print("Unknown command. Press ? for help.")
        action()

        if self.mode == "EXPLORE":
            self.prompt = "[M] to move, [A] to hunt"
        elif self.mode == "ENCOUNTER":
            self.prompt = "[A] to attack, [F] to flee"
        elif self.mode == "ENCOUNTER_END":
            self.prompt = "[L] to leave"

    def cmd_help(self):
        if(self.mode == "EXPLORE"):
            #print(f"{self.location} with enemies: {self.location.print_enemies()}")
            pass
        else:
            enemy = self.encounter
            #print(f"Combat with {enemy.name} with [{enemy.hp} HP]")


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
        log = [("Hit for ", "normal"), (f"-{dmg_amount}", "damage"), (" HP", "hp_value")]
        self.message_logs.encounter.combat.add_line(log)
        self.update_encounter_info()

        if not self.is_encounter_alive():
            log = [(f"{self.player.name} killed {self.encounter.name} and gained {self.encounter.xp}xp", "normal")]
            self.message_logs.encounter.end.add_line(log)

            #reset
            self.location.remove_enemy(self.encounter)
            self.message_logs.encounter.clear_combat_logs()
            self.encounter = None
            self.mode = "ENCOUNTER_END"

    def cmd_leave(self):
        if self.mode == "ENCOUNTER_END":
            self.message_logs.encounter.clear_logs()
            self.mode = "EXPLORE"


    def is_encounter_alive(self):
        return self.encounter.alive

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

    def print_combat_log(self):
        self.stdscr.addstr(5, 0, "")
        for line in self.combat_log[-4:]:
            for text, attr in line:
                self.stdscr.addstr(text, attr)
            self.stdscr.addstr("\n")

    def update_player_log(self):
        log = [
            (f"{self.player.name} [", "normal"),
            (f"{self.player.hp}", "hp_value"),
            (f"] HP", "normal")
        ]
        self.player_log = log

    def update_encounter_info(self):
        if(self.encounter != None):
            log = [
                (f"{self.encounter.name} [", "normal"),
                (f"{self.encounter.hp}", "hp_value"),
                (f"] HP", "normal")
            ]
            self.message_logs.encounter.enemy.add_line(log)
            log = [
                (f"{self.encounter.name} [", "normal"),
                (f"{self.encounter.hp}", "hp_value"),
                (f"] HP", "normal")
            ]
            self.encounter_log = log











