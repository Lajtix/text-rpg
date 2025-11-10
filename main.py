from models.player import Character
from models.location import Location
from game_model import GameModel
from ui.game_view import GameView
import curses

def main(stdscr):



    NPC1 = Character("Greg", 5, 11)
    NPC2 = Character("Greg", 10, 22)
    NPC3 = Character("Bear", 15, 33)
    NPC4 = Character("Greg", 20, 44)
    NPC5 = Character("Bear", 20, 8)
    Player = Character("Luba", 7, 2)
    enemies = [NPC1, NPC2, NPC3, NPC4]

    # console.print("[bold green]Welcome hero![/]")

    dark_forest = Location("Dark Forest", "Bear")
    dark_forest.add_enemy(NPC5)
    dark_forest.add_enemy(NPC4)
    dark_forest.print_info()
    NPC4.level = 1


    Player.level = 1
    model = GameModel(Player, dark_forest)
    view = GameView(stdscr, model)



    while True:
        stdscr.clear()
        #cmd = stdscr.get_wch()
        #action = model.commands[model.mode][cmd]
        #if not action:
        #    print("Unknown command. Press ? for help.")
        #    continue
        #action()
        # 1. View draws the screen
        view.draw()

        # 2. CONTROLLER (main) gets the input
        key = stdscr.get_wch() # <-- IT MOVES HERE

        # 3. Controller checks for global quit
        if key in [ord('q'), ord('Q')]:
            break

        # 4. Controller passes the input to the Model
        model.process_command(key)

if __name__ == "__main__":
    curses.wrapper(main)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



