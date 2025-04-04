class LevelSystem:
    def __init__(self):
        self.thresholds = self._generate_thresholds()
        self.xp = 0
        self.level = 1

    def _generate_thresholds(self):
        # Generate XP thresholds for levels 1-10 using the formula from the image
        return [10 + 5 * (n ** 1.5) for n in range(1, 11)]

    def add_xp(self, amount):
        self.xp += amount
        self._check_level_up()

    def _check_level_up(self):
        new_level = 1
        for threshold in self.thresholds:
            if self.xp >= threshold:
                new_level += 1
            else:
                break

        if new_level > self.level:
            self.level = new_level
            print(f"    |    You are now level {self.level}!")

    def save_data(self):
        return f"XP:{self.xp}\nLEVEL:{self.level}"

    def load_data(self, data):
        for line in data.split('\n'):
            if line.startswith('XP:'):
                self.xp = int(line.split(':')[1])
            elif line.startswith('LEVEL:'):
                self.level = int(line.split(':')[1])
        self._check_level_up()  # In case loaded XP qualifies for higher level