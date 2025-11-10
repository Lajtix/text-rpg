from player import Character
from location import Location

from game import Game
import curses



NPC1 = Character("Greg", 5, 11)
NPC2 = Character("Greg", 10, 22)
NPC3 = Character("Bear", 15, 33)
NPC4 = Character("Greg", 20, 44)
NPC5 = Character("Bear", 20, 8)
Player = Character("Luba", 7, 2)
enemies = [NPC1, NPC2, NPC3, NPC4]

#console.print("[bold green]Welcome hero![/]")

dark_forest = Location("Dark Forest", "Bear")
dark_forest.add_enemy(NPC5)
dark_forest.add_enemy(NPC4)
dark_forest.print_info()
NPC4.level = 1

Player.level = 1


Game = Game(Player, dark_forest)
#Game.start()
Game.start()


