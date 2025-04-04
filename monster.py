from character import Character


class Monster(Character):
    def __init__(self):
        super().__init__()

    # Determines the behavior of the monster based on the hero's health points and experience, and the monster's health points
    def determine_behavior(self, hero):
        if hasattr(hero, 'level_system'):
            player_xp = hero.level_system.xp
            hp = hero.health_points

            if hp > 50:
                if player_xp >= 30:
                    if self.health_points > 15:
                        print("The monster is very strong and attacks aggressively!")
                    elif self.health_points > 10:
                        print(" -- The monster is strong but hesitant.")
                    else:
                        print(" -- The monster attacks cautiously.")
                else:
                    if self.health_points > 10:
                        print(" -- The monster is unsure but prepares to fight.")
                    else:
                        print(" -- The monster watches you warily.")
            else:
                if player_xp < 10:
                    if self.health_points < 5:
                        print(" -- The weak monster observes your movements.")
                    else:
                        print(" -- The monster watches you carefully.")
                else:
                    if self.health_points > 15:
                        print(" -- The strong monster senses weakness and attacks aggressively!")
                    elif self.health_points > 5:
                        print(" -- The monster hesitates but attacks anyway.")
                    else:
                        print(" -- The weak monster makes a last-ditch attack!")

    def attack(self, hero):
        self.determine_behavior(hero)  # Show behavior before attacking
        print(f"Monster attacks with {self.combat_strength} strength!")
        hero.health_points -= self.combat_strength
        if hero.health_points <= 0:
            print("Hero has fallen!")

    def __del__(self):
        print("The Monster object is being destroyed by the garbage collector")
        super().__del__()