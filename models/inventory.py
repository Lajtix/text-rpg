import time
class Inventory:
    def __init__(self):
        #self.icon_list = ["†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†", "†"]
        self.icon_list = ["😁"]# "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️", "⚔️"]
        self.index = 0
        self.num_of_cols = 5
        self.num_of_rows = 4
        ICONS = {
            "weapon": "†",
            "shield": "▣",
            "potion": "○",
            "gem": "◆",
            "key": "⌑",
            "bag": "⧉",
            "food": "¤",
            "scroll": "⌘",
        }

    def move_left(self):
        if(self.index > 0):
            self.index = self.index - 1

    def move_right(self):
        if (self.index < self.num_of_cols * self.num_of_rows):
            self.index = self.index + 1

    def get_index(self):
        return self.index
