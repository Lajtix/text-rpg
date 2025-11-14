from models.logs import Log
import curses

class EncounterView:
    def __init__(self, stdscr, encounter_logs, win_row_ranges, win_col_ranges, model):
        self.stdscr = stdscr
        self.logs = encounter_logs
        self.win_row_ranges = win_row_ranges
        self.win_col_ranges = win_col_ranges
        self.model = model
        self.i = 0
        self.style_map = {
            "normal": curses.A_NORMAL,
            "damage": curses.color_pair(1) | curses.A_BOLD,
            "hp_value": curses.color_pair(1)
        }

    def draw_encounter(self):
        if (self.model.mode == "ENCOUNTER" or self.model.mode == "ENCOUNTER_END"):
            self.draw_enemy()
            self.draw_combat_log()
            if(self.model.message_logs.encounter.flee != None):
                self.draw_flee()

        if(self.model.mode == "ENCOUNTER_END"):
            self.draw_end_log()



    def draw_combat_log(self):
        row_min, row_max = self.win_row_ranges["combat_log"]
        col_min, col_max = self.win_col_ranges["combat_log"]
        log = self.logs.combat
        y = row_min
        x = col_min + 1
        for line in log.lines:
            self.stdscr.addstr(y, x, "")
            y = y + 1
            for text, attr in line:
                self.stdscr.addstr(text, self.style_map[attr])


    def draw_enemy(self):
        encounter = self.model.encounter
        row_min, row_max = self.win_row_ranges["player_enemy"]
        col_min, col_max = self.win_col_ranges["enemy"]
        y = row_min
        x = col_min
        col = (int)((col_max - col_min - len(encounter.name)) / 2 + col_min)
        self.stdscr.addstr(row_min, col_min + 1, f"Name: {encounter.name}", self.style_map["normal"])
        self.stdscr.addstr(row_min, col_min + 40, f"LV: {encounter.level}", self.style_map["normal"])
        self.stdscr.addstr(row_min + 1, col_min + 1, "HP: [", self.style_map["normal"])
        self.stdscr.addstr(f"{encounter.hp}", self.style_map["hp_value"])
        self.stdscr.addstr(f"/", self.style_map["normal"])
        self.stdscr.addstr(f"{encounter.max_hp}", self.style_map["hp_value"])
        self.stdscr.addstr(f"]", self.style_map["normal"])

    def draw_end_log(self):
        row_min, row_max = self.win_row_ranges["encounter"]
        col_min, col_max = self.win_col_ranges["encounter"]
        text, attr = self.model.message_logs.encounter.end.lines[0][0]
        self.stdscr.addstr(row_max, col_min + 1, text, self.style_map[attr])

    def draw_flee(self):
        row_min, row_max = self.win_row_ranges["encounter"]
        col_min, col_max = self.win_col_ranges["encounter"]
        self.stdscr.addstr(row_max, col_min + 1, "gggga", self.style_map["normal"])
        text, attr = self.model.message_logs.encounter.flee.lines[0][0]
        self.stdscr.addstr(row_max, col_min + 1, "gggga", self.style_map[attr])