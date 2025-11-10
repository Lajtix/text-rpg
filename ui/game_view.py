from ui.encounter_view import EncounterView
from game_model import GameModel
from ui.ui_layout import UILayout
from models.logs import MessageLogs
import curses
class GameView:
    def __init__(self, stdscr, model: GameModel):
        self.stdscr = stdscr
        self.model = model
        self.message_logs = MessageLogs()
        self.UI = UILayout(self.stdscr, self.model)
        self.encounter_view = self.UI.encounter_view

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.style_map = {
            "normal": curses.A_NORMAL,
            "hp_value": curses.color_pair(1) | curses.A_BOLD,
            "default": curses.A_NORMAL
        }

    def draw(self):
        self.UI.draw()







        self.stdscr.noutrefresh()
        curses.doupdate()


    def draw_encounter_logs(self):
        self.encounter_view.print_encounter_info()


