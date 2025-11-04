
class Location:
    def __init__(self, name, typicalEnemy):
        self.name = name
        self.typicalEnemy = typicalEnemy
        self.enemies = []

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def print_info(self):
        print(f"You are in {self.name.capitalize()}")
        print(f"Enemies are: ")
        self.print_enemies()

    def print_enemies(self):
        for i, enemy in enumerate(self.enemies):
            if i == len(self.enemies) - 1:
                print(f"{enemy.name} [{enemy.hp} HP]")
            else:
                print(f"{enemy.name} [{enemy.hp} HP], ")
