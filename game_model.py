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
        self.message_logs =  MessageLogs()
        self.can_flee = True
        self.mode = "EXPLORE"
        self.encounter = None
        self.prompt = "[M] to move, [A] to hunt"
        self.commands = {
            "EXPLORE" : {
                "M" : self.cmd_move,
                "A" : self.cmd_hunt,
                "I" : self.cmd_inventory,
            },
            "ENCOUNTER": {
                "A" : self.cmd_attack,
                "F" : self.cmd_flee,
            },
            "ENCOUNTER_END": {
                "L" : self.cmd_leave,
            },
            "INVENTORY" : {
                "A" : self.player.inventory.move_left,
                "W" : self.player.inventory.move_right,
            }
        }
    def run(self, stdscr):
        self.main_game_loop()

    def process_command(self, cmd):
        if cmd == None:
            return
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
        self.encounter.take_damage(dmg_amount, self.player, self.message_logs.encounter.combat)
        self.update_encounter_info()

        self.cmd_end_of_encounter()

    def cmd_end_of_encounter(self):
        if not self.is_encounter_alive():
            log = [(f"{self.player.name} killed {self.encounter.name} and gained {self.encounter.xp}xp", "normal")]
            self.message_logs.encounter.end.add_line(log)
            self.mode = "ENCOUNTER_END"

    def cmd_leave(self):
        if self.mode == "ENCOUNTER_END":
            self.location.remove_enemy(self.encounter)
            self.message_logs.encounter.clear_combat_logs()
            self.encounter = None
            self.mode = "EXPLORE"


    def is_encounter_alive(self):
        return self.encounter.alive

    def cmd_flee(self):
        if (self.can_flee):
            if (self.encounter.flee(self.player) == 1):
                #self.encounter = None
                self.mode = "ENCOUNTER_END"
                log = [("Flee was successful", "normal")]
                self.message_logs.encounter.end.add_line(log)
            else:
                log = [("Flee was not successful", "normal")]
                self.message_logs.encounter.end.add_line(log)
                self.can_flee = False
        else:
            pass


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

    def cmd_inventory(self):
        self.mode = "INVENTORY"











