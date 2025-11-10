from .encounter_view import EncounterView
from models.logs import EncounterLogs

class UILayout:
    def __init__(self, stdscr, model):
        self.model = model
        self.stdscr = stdscr
        self.win_header = None
        self.win_left_player = None
        self.win_right_enemy = None
        self.win_encounter = None
        self.win_combat_log = None
        self.win_system_log = None
        self.player = self.model.player
        self.location = self.model.location

        self.logs = self.model.message_logs


        self.win_h = {
            "header" : 3,
            "player_enemy" : 12,
            "encounter" : 7,
            "combat_log" : 6,
            "system_log" : 3,
            }

        self.win_row_ranges = {
            "player_enemy" : (self.win_h["header"] + 1, self.win_h["header"] + self.win_h["player_enemy"] - 2),
            "encounter" : (self.win_h["header"] + self.win_h["player_enemy"] + 1, self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] - 2),
            "combat_log": (self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] + 1, self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] + self.win_h["combat_log"] -2),
            "system_log": (self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] + self.win_h["combat_log"] + 1, self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] + self.win_h["combat_log"] + self.win_h["system_log"] - 2),
        }

        self.win_col_ranges = {
            "header" : (1, 99),
            "player" : (1, 49),
            "enemy" : (51, 99),
            "encounter" : (1, 99),
            "combat_log": (1, 99),
            "system_log": (1, 99),
        }

        self.encounter_view = EncounterView(self.stdscr, self.logs.encounter, self.win_row_ranges["encounter"], self.win_col_ranges["encounter"])

    def draw(self):
        self.init_windows()
        self.draw_windows()
        self.draw_headlines()
        self.draw_descriptions()
        self.draw_header()
        self.draw_encounter_info()

        self.draw_system()

    def init_windows(self):
        header_xy = 0
        header_h = 3

        player_enemy_h = 12
        width = 100
        encounter_y = 12
        encounter_h = 7
        combat_log_h = 6
        system_log_h = 3

        self.win_header = self.stdscr.derwin(header_h, width, 0, header_xy,)
        self.win_left_player = self.stdscr.derwin(player_enemy_h, int(width/2), self.win_h["header"], header_xy)
        self.win_right_enemy = self.stdscr.derwin(player_enemy_h, int(width / 2), self.win_h["header"], header_xy + int(width/2))
        self.win_encounter = self.stdscr.derwin(encounter_h, width, self.win_h["header"] + self.win_h["player_enemy"], header_xy)
        self.win_combat_log = self.stdscr.derwin(combat_log_h, width, self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"], header_xy)
        self.win_system_log = self.stdscr.derwin(system_log_h, width, self.win_h["header"] + self.win_h["player_enemy"] + self.win_h["encounter"] + self.win_h["combat_log"], header_xy)

    def draw_windows(self):
        self.win_header.box()
        self.win_left_player.box()
        self.win_right_enemy.box()
        self.win_encounter.box()
        self.win_combat_log.box()
        self.win_system_log.box()

        self.win_header.noutrefresh()
        self.win_left_player.noutrefresh()
        self.win_right_enemy.noutrefresh()
        self.win_encounter.noutrefresh()
        self.win_combat_log.noutrefresh()
        self.win_system_log.noutrefresh()


    def draw_headlines(self):
        self.stdscr.addstr(3, 22, f" Player ")
        self.stdscr.addstr(3, 71, f" Enemy ")
        self.stdscr.addstr(15, 40, f" Encounter / Story Area ")
        self.stdscr.addstr(22, 44, f" Combat Log ")
        self.stdscr.addstr(28, 44, f" System/Help ")
        #self.stdscr.refresh()

    def draw_descriptions(self):
        self.draw_header()

    def draw_header(self):
        self.stdscr.addstr(1, 1, f"Player: {self.player.name} | LV {self.player.level} | HP {self.player.hp}/{self.player.max_hp} | "
                                 f"XP {self.player.xp}/{self.player.level_ups_list[self.player.level]} | Gold: {self.player.gold} | "
                                 f"Area: {self.location.name}")

    def draw_system(self):
        min_y, max_y = self.win_row_ranges["system_log"]
        self.stdscr.addstr(min_y, 1,
                           f"{self.model.prompt}")

    def draw_encounter_info(self):
        '''
        min_y, max_y = self.win_row_ranges["player_enemy"]
        self.stdscr.addstr(min_y, 0, "GG", 0)
        self.stdscr.addstr(max_y, 0, "KK", 0)

        for min_y, max_y in self.win_row_ranges.values():
            self.stdscr.addstr(min_y, 0, "GG", 0)
            self.stdscr.addstr(max_y, 0, "KK", 0)
        '''

        self.encounter_view.draw_combat_log()