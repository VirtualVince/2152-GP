from character import Character

class Hero(Character):
    def __init__(self):
        super().__init__()

    def attack(self, monster):
        print(f"Hero attacks with {self.combat_strength} strength!")
        monster.health_points -= self.combat_strength
        if monster.health_points <= 0:
            print("Monster defeated!")

    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()
