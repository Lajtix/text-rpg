class EncounterView:
    def __init__(self, stdscr, encounter_logs_model):
        self.logs_model = encounter_logs_model
        self.stdscr = stdscr


    def print_encounter_info(self):
        for log in self.logs_model:
            x = log.x
            for line in log.lines:
                self.stdscr.addstr(x, log.y, "")
                x = x + 1
                for text, attr in line:
                    self.stdscr.addstr(text, attr)