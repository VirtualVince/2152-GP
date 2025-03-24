from character import Character

class Monster(Character):
    def __init__(self):
        super().__init__()

    def attack(self, hero):
        print(f"Monster attacks with {self.combat_strength} strength!")
        hero.health_points -= self.combat_strength
        if hero.health_points <= 0:
            print("Hero has fallen!")

    def __del__(self):
        print("The Monster object is being destroyed by the garbage collector")
        super().__del__()
