from models.logs import Log
import curses


class EncounterView:
    def __init__(self, stdscr, encounter_logs, win_row_ranges, win_col_ranges):
        self.stdscr = stdscr
        self.logs = encounter_logs
        self.row_min, self.row_max = win_row_ranges
        self.col_min, self.col_max = win_col_ranges
        self.style_map = {
            "normal": curses.A_NORMAL,
            "damage": curses.color_pair(1) | curses.A_BOLD,
            "hp_value": curses.A_NORMAL
        }

    def draw_combat_log(self):

        log = self.logs.combat
        y = self.row_min
        x = self.col_min
        for line in log.lines:
            self.stdscr.addstr(y, x, "")
            y = y + 1
            for text, attr in line:
                self.stdscr.addstr(text, self.style_map[attr])
