import random
from random import randint
import math
import curses
import os
from ui.ui_layout import UILayout
from models.logs import MessageLogs, EncounterLogs
from ui.encounter_view import EncounterView
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self, player, location):
        self.stdscr = None

        self.player = player
        self.location = location
        self.locations = []
        #self.message_logs = None
        self.message_logs = None
        self.can_flee = True
        self.mode = "EXPLORE"
        self.encounter = None
        self.UI = None

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

    def start(self):
        curses.wrapper(self.run)  # <- this is where curses starts!

    def run(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.mousemask(0)
        self.stdscr.keypad(True)
        self.stdscr.nodelay(False)

        #Enable colors and define them
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        self.main_game_loop()

    def main_game_loop(self):
        self.message_logs = MessageLogs(self.stdscr)
        self.UI = UILayout(self.stdscr, self.player, self.location, self.message_logs)

        while True:
            #initialize
            self.stdscr.erase()
            self.UI.init_windows()
            self.UI.draw_windows()
            self.UI.draw_descriptions()
            self.UI.draw_header()
            self.UI.draw_headlines()
            self.stdscr.refresh()

            #main loop
            if self.mode == "EXPLORE":
                prompt = "[M] to move, [A] to hunt"
            elif self.mode == "ENCOUNTER":
                prompt = "[A] to attack, [F] to flee"
            elif self.mode == "ENCOUNTER_END":
                prompt = "[L] to leave"

            self.stdscr.addstr(10, 0, f"{prompt}")
            self.UI.draw_encounter_info()
            self.stdscr.refresh()
            cmd = self.stdscr.get_wch()


            action = self.commands[self.mode][cmd]
            if not action:
                print("Unknown command. Press ? for help.")
                continue
            action()
            self.stdscr.refresh()


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
        log = [("Hit for ", 0), (f"-{dmg_amount}", curses.color_pair(1)), (" HP", 2)]
        self.message_logs.encounter.combat.add_line(log)
        self.update_encounter_info()

        if not self.is_encounter_alive():
            log = [(f"{self.player.name} killed {self.encounter.name} and gained {self.encounter.xp}xp", 0)]
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
            (f"{self.player.name} [", 0),
            (f"{self.player.hp}", curses.color_pair(1)),
            (f"] HP", 0)
        ]
        self.player_log = log

    def update_encounter_info(self):
        if(self.encounter != None):
            log = [
                (f"{self.encounter.name} [", 0),
                (f"{self.encounter.hp}", curses.color_pair(1)),
                (f"] HP", 0)
            ]
            self.message_logs.encounter.enemy.add_line(log)
            log = [
                (f"{self.encounter.name} [", 0),
                (f"{self.encounter.hp}", curses.color_pair(1)),
                (f"] HP", 0)
            ]
            self.encounter_log = log

    def print_encounter_info(self):
        for log in self.message_logs.encounter:
            x = log.x
            for line in log.lines:
                self.stdscr.addstr(x, log.y, "")
                x = x + 1
                for text, attr in line:
                    self.stdscr.addstr(text, attr)











