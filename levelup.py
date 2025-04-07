class LevelSystem:
    # Initialize the level system and generate XP threshold
    def __init__(self):
        self.thresholds = self._generate_thresholds()
        self.xp = 0
        self.level = 1

    # Generate XP thresholds for levels 1-10
    def _generate_thresholds(self):
        return [10 + 5 * (n ** 1.5) for n in range(1, 11)]

    # Method to add XP
    def add_xp(self, amount):
        self.xp += amount
        self._check_level_up()

    # Method to check if the hero should level up
    def _check_level_up(self):
        new_level = 1
        for threshold in self.thresholds:
            if self.xp >= threshold:
                new_level += 1
            else:
                break

        # Check if the new level is higher than the current level, and if so, level up
        if new_level > self.level:
            self.level = new_level
            print(f"    |    You are now level {self.level}!")

    # Method to load data regarding player XP and levels
    def load_data(self, data):
        for line in data.split('\n'):
            if line.startswith('XP:'):
                self.xp = int(line.split(':')[1])
            elif line.startswith('LEVEL:'):
                self.level = int(line.split(':')[1])
        self._check_level_up()