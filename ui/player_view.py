import curses
import time
#from wcwidth import wcwidth
class PlayerView():
    def __init__(self, player, stdscr, win_row_ranges, win_col_ranges, model):
        self.player = player
        self.stdscr = stdscr
        self.win_row_ranges = win_row_ranges
        self.win_col_ranges = win_col_ranges
        self.model = model

        self.style_map = {
            "normal": curses.A_NORMAL,
            "damage": curses.color_pair(1) | curses.A_BOLD,
            "hp_value": curses.color_pair(1)
        }

        self.time_interval = 0.5
        self.last_blink_time = time.time()
        self.blink_on = True

    def draw_inventory(self):
        min_row, max_row = self.win_row_ranges["player_enemy"]
        start_row = max_row - 4
        min_col, max_col = self.win_col_ranges["player"]
        start_col = max_col - 20
        #self.stdscr.addstr(start_row - 1, start_col, f"INDEX: {self.player.inventory.get_index()}", self.style_map["normal"])
        for i, item in enumerate(self.player.inventory.icon_list, start=1):
            if i % 5 == 1:
                self.draw_item(start_row, start_col, f"{self.player.inventory.icon_list[i-1]} ", self.style_map["normal"])
                #self.stdscr.addstr(start_row, start_col, f"{self.player.inventory.icon_list[i-1]} ", self.style_map["normal"])
            elif i % 5 == 0:
                start_row = start_row + 1
            else:
                self.draw_item(start_row, start_col, f"{self.player.inventory.icon_list[i - 1]} ", self.style_map["normal"])
                y, x = self.stdscr.getyx()
                #self.stdscr.addstr(y, x, f"{self.player.inventory.icon_list[i-1]} ", self.style_map["normal"])


    def draw_item(self, y, x, text, attr):
        col = x
        for ch in text:
            #w = wcwidth(ch)
            w =4
            self.stdscr.addstr(y, col, ch, attr)
            self.stdscr.addstr(y, col + 1, " ", attr)
            if w < 0:
                w = 1
            col += w

    def select_item(self):
        min_row, max_row = self.win_row_ranges["player_enemy"]
        start_row = max_row - 3
        min_col, max_col = self.win_col_ranges["player"]
        start_col = max_col - 20
        now=time.time()
        if(now - self.last_blink_time > self.time_interval):
            self.blink_on = not self.blink_on
            self.last_blink_time = now

        if self.blink_on:
            row = start_row + (int)(self.player.inventory.get_index() / (self.player.inventory.num_of_rows + 1))
            col = start_col + 2 * (self.player.inventory.get_index() %  self.player.inventory.num_of_cols)
            self.stdscr.addstr(row, col, " ", self.style_map["normal"])
        else:
            #self.stdscr.addstr(start_row, start_col, "G ", self.style_map["normal"])
            pass

