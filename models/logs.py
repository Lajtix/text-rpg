class Log:
    def __init__(self, max_lines, y, x):
        self.max_lines = max_lines
        self.x = x
        self.y = y
        self.coordinates = (self.x, self.y)
        self.lines = []

    def add_line(self, line):
        if not (len(self.lines) < self.max_lines):
            del self.lines[0]
        self.lines.append(line)

class EncounterLogs:
    def __init__(self):
        self.combat = Log(4, 5, 0)
        self.loot = Log(20, 12, 0)
        self.end = Log(3, 3, 0)
        self.enemy = Log(1, 0, 18)

    def __iter__(self):
        yield self.combat
        yield self.loot
        yield self.end
        yield self.enemy

    def clear_combat_logs(self):
        self.combat.lines.clear()

    def clear_logs(self):
        for log in self:
            log.lines.clear()

class MessageLogs:
    def __init__(self):
        self.encounter = EncounterLogs()
