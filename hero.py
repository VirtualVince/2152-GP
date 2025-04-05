from character import Character
from levelup import LevelSystem

class Hero(Character):
    def __init__(self):
        super().__init__()
        self.level_system = LevelSystem() # Initialize the level system for the hero

    def attack(self, monster):
        print(f"Hero attacks with {self.combat_strength} strength!")
        monster.health_points -= self.combat_strength
        if monster.health_points <= 0:
            print("Monster defeated!")
            # Grant XP when defeating a monster
            xp_gained = monster.combat_strength # XP gained is equal to monster's combat strength
            self.level_system.add_xp(xp_gained) 
            print(f"    |    Gained {xp_gained} XP!") # Print the amount of XP gained

    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()