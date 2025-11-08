import random
from random import randint
import math
from rich.console import Console
import curses
import os



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


console = Console()
class Game:
    def __init__(self, player, location):
        self.player = player
        self.location = location
        self.locations = []
        self.can_flee = True
        self.mode = "EXPLORE"
        self.encounter = None
        self.stdscr = None
        self.combat_log = []
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
            }
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
        while True:


            self.stdscr.erase()
            if self.mode == "EXPLORE":
                prompt = "[M] to move, [A] to hunt"
            else:
                prompt = "[A] to attack, [F] to flee"
            self.print_player_info()
            self.print_combat_log()
            self.print_encounter_info()
            self.stdscr.addstr(10, 0, f"{prompt}")
            self.stdscr.refresh()
            cmd = self.stdscr.get_wch()
            self.stdscr.refresh()
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
        #console.print(f"Hit for  [[red]-{dmg_amount}[/red] HP].")
        #console.print(f"{self.encounter.name} has [[red]{self.encounter.hp}[/red] HP].")

        log = [("Hit for ", 0), (f"-{dmg_amount}", curses.color_pair(1)), (" HP", 2)]
        self.log_append(log)

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

    def log_append(self, log):
        self.combat_log.append(log)

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
            self.encounter_log = log

    def print_encounter_info(self):
        self.update_encounter_info()
        self.stdscr.addstr(0, 18, "")

        for text, attr in self.encounter_log:
            self.stdscr.addstr(text, attr)

    def print_player_info(self):
        self.update_player_log()
        self.stdscr.addstr(0, 0, "")

        for text, attr in self.player_log:
            self.stdscr.addstr(text, attr)








