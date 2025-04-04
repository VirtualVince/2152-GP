# Import required modules
import random
import os
import platform
from hero import Hero
from monster import Monster

# Print system details
print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

# Define Dice, Weapons, Loot, and Monster Powers
small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]

loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
belt = []

monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

num_stars = 0  # Stars to award the player


# --- Input Validation for Combat Strength ---
i = 0
input_invalid = True
while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    combat_strength_input = input("Enter your combat Strength (1-6): ")
    print("    |", end="    ")
    m_combat_strength_input = input("Enter the monster's combat Strength (1-6): ")

    if (not combat_strength_input.isdigit()) or (not m_combat_strength_input.isdigit()):
        print("    |    One or more invalid inputs. Please enter integer numbers for Combat Strength")
        i += 1
        continue
    cs = int(combat_strength_input)
    mcs = int(m_combat_strength_input)
    if cs not in range(1, 7) or mcs not in range(1, 7):
        print("    |    Enter a valid integer between 1 and 6 only")
        i += 1
        continue
    else:
        input_invalid = False
        break

if input_invalid:
    print("Too many invalid attempts. Exiting the game.")
    exit()

# --- Instantiate Hero and Monster Objects ---
hero = Hero()
monster = Monster()

# Store the initial combat strengths
hero_initial_cs = cs
monster_initial_cs = mcs

# Load XP data
try:
    with open("save.txt", "r") as file:
        lines = file.readlines()
        if len(lines) > 1:  # If XP data exists
            hero.level_system.load_data(lines[1].strip())
            print(f"    |    Welcome back! You are level {hero.level_system.level} with {hero.level_system.xp} XP.")

            # Calculate total combat strength
            level_bonus = hero.level_system.level // 2
            total_combat = hero_initial_cs + level_bonus
            print(
                f"    |    Because you are level {hero.level_system.level}, +{level_bonus} has been added to your combat strength.")
            print(
                f"    |    The hero's combat strength is now {total_combat}. (base {hero_initial_cs} + level bonus {level_bonus})")

            # Set the actual combat strength
            hero.combat_strength = total_combat
            monster.combat_strength = monster_initial_cs

except FileNotFoundError:
    # in the case of a new game with no save data
    hero.combat_strength = hero_initial_cs
    monster.combat_strength = monster_initial_cs

# --- Weapon Roll ---
print("    |", end="    ")
input("Roll the dice for your weapon (Press enter)")
ascii_image_weapon = """
              , %               .           
   *      @./  #         @  &.(         
  @        /@   (      ,    @       # @ 
  @        ..@#% @     @&*#@(         % 
   &   (  @    (   / /   *    @  .   /  
     @ % #         /   .       @ ( @    
                 %   .@*                
               #         .              
             /     # @   *              
                 ,     %                
            @&@           @&@
"""
print(ascii_image_weapon)

weapon_roll = random.choice(small_dice_options)
# Adjust hero's combat strength based on weapon roll (removed max of 6)
hero.combat_strength += weapon_roll
print("    |    The hero's weapon is " + str(weapons[weapon_roll - 1]))

def load_previous_game():
    try:
        with open("save.txt", "r") as file:
            lines = [line.strip() for line in file.readlines()]
            if not lines:
                return 0, 0, 1, None  # (kills, xp, level, winner)

            kills = int(lines[0]) if lines[0].isdigit() else 0
            xp = int(lines[1].split(":")[1]) if len(lines) > 1 and "XP:" in lines[1] else 0
            level = int(lines[2].split(":")[1]) if len(lines) > 2 and "LEVEL:" in lines[2] else 1
            winner = lines[3].split(": ")[1] if len(lines) > 3 and "Won:" in lines[3] else None

            return kills, xp, level, winner
    except (FileNotFoundError, IndexError, ValueError):
        return 0, 0, 1, None  # (kills, xp, level, winner)


# --- Adjust Combat Strength Based on Previous Game ---
last_kills, loaded_xp, loaded_level, last_winner = load_previous_game()
hero.level_system.xp = loaded_xp
hero.level_system.level = loaded_level

if last_kills > 0:
    print(f"    |    Currently, you are Level {hero.level_system.level}, with {last_kills} total kills.")

    #Adjust combat strength based on last winner
    if last_winner == "Hero":
        level_bonus = min(2, hero.level_system.level)
        print(f"    |    After your last victory, monsters grew stronger (+{level_bonus}) to monster combat scores.")
        monster.combat_strength = monster.combat_strength + level_bonus
        print(f"    |    The monster's new combat score is {monster.combat_strength}.")
    elif last_winner == "Monster":
        kill_bonus = min(2, last_kills // 3)
        print(f"    |    After your last defeat, you trained harder. (+{kill_bonus}) to your combat score.")
        hero.combat_strength = hero.combat_strength + kill_bonus
        print(f"    |    Your new combat score is {hero.combat_strength}.")
    else:
        print("    |    The land remains balanced for your journey")

# --- Weapon Roll Analysis ---
print("    ------------------------------------------------------------------")
print("    |", end="    ")
input("Analyze the Weapon roll (Press enter)")
print("    |", end="    ")
if weapon_roll <= 2:
    print("--- You rolled a weak weapon, friend")
elif weapon_roll <= 4:
    print("--- Your weapon is meh")
else:
    print("--- Nice weapon, friend!")
if weapons[weapon_roll - 1] != "Fist":
    print("    |    --- Thank goodness you didn't roll the Fist...")

# --- Roll for Health Points ---
print("    |", end="    ")
input("Roll the dice for your health points (Press enter)")
hero.health_points = random.choice(big_dice_options)
print("    |    Player rolled " + str(hero.health_points) + " health points")

print("    |", end="    ")
input("Roll the dice for the monster's health points (Press enter)")
monster.health_points = random.choice(big_dice_options)
print("    |    Monster rolled " + str(monster.health_points) + " health points")

# --- Loot Collection ---
print("    ------------------------------------------------------------------")
print("    |    !!You find a loot bag!! You look inside to find 2 items:")
print("    |", end="    ")
input("Roll for first item (Press enter)")

def collect_loot(loot_options, belt):
    ascii_image_loot = """
                      @@@ @@                
             *# ,        @              
           @           @                
                @@@@@@@@                
               @   @ @% @*              
            @     @   ,    &@           
          @                   @         
         @                     @        
        @                       @       
        @                       @       
        @*                     @        
          @                  @@         
              @@@@@@@@@@@@          
              """
    print(ascii_image_loot)
    loot_roll = random.choice(range(1, len(loot_options) + 1))
    loot = loot_options.pop(loot_roll - 1)
    belt.append(loot)
    print("    |    Your belt: ", belt)
    return loot_options, belt

loot_options, belt = collect_loot(loot_options, belt)
print("    ------------------------------------------------------------------")
print("    |", end="    ")
input("Roll for second item (Press enter)")
loot_options, belt = collect_loot(loot_options, belt)
print("    |    You're super neat, so you organize your belt alphabetically:")
belt.sort()
print("    |    Your belt: ", belt)

# --- Use Loot ---
def use_loot(belt, health_points):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]
    print("    |    You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)
    if first_item in good_loot_options:
        health_points = min(20, (health_points + 2))
        print("    |    You used " + first_item + " to up your health to " + str(health_points))
    elif first_item in bad_loot_options:
        health_points = max(0, (health_points - 2))
        print("    |    You used " + first_item + " to hurt your health to " + str(health_points))
    else:
        print("    |    You used " + first_item + " but it's not helpful")
    return belt, health_points

belt, hero.health_points = use_loot(belt, hero.health_points)

# --- Analysis of Roll ---
print("    ------------------------------------------------------------------")
print("    |", end="    ")
input("Analyze the roll (Press enter)")
print("    |    --- You are matched in strength: " + str(hero.combat_strength == monster.combat_strength))
print("    |    --- You have a strong player: " + str((hero.combat_strength + hero.health_points) >= 15))

# --- Monster Magic Power ---
print("    |", end="    ")
input("Roll for Monster's Magic Power (Press enter)")
ascii_image_magic = """
                @%   @                      
         @     @                        
             &                          
      @      .                          
     @       @                    @     
              @                  @      
      @         @              @  @     
       @            ,@@@@@@@     @      
         @                     @        
            @               @           
                 @@@@@@@                
"""
print(ascii_image_magic)
power_roll = random.choice(list(monster_powers.keys()))
monster.combat_strength = monster.combat_strength + monster_powers[power_roll] # removed cap of 6
print("    |    The monster's combat strength is now " + str(monster.combat_strength) + " using the " + power_roll + " magic power")

# --- Inception Dream (Recursive Function) ---
def inception_dream(num_dream_lvls):
    num_dream_lvls = int(num_dream_lvls)
    if num_dream_lvls == 1:
        print("    |    You are in the deepest dream level now")
        print("    |", end="    ")
        input("Start to go back to real life? (Press Enter)")
        print("    |    You start to regress back through your dreams to real life.")
        return 2
    else:
        return 1 + inception_dream(num_dream_lvls - 1)

num_dream_lvls = -1
while not (0 <= num_dream_lvls <= 3):
    try:
        num_dream_lvls = int(input("How many dream levels do you want to go down? (Enter a number 0-3): "))
        if not (0 <= num_dream_lvls <= 3):
            print("Number entered must be a whole number between 0-3 inclusive, try again")
            num_dream_lvls = -1
        elif num_dream_lvls != 0:
            hero.health_points -= 1
            crazy_level = inception_dream(num_dream_lvls)
            hero.combat_strength = hero.combat_strength + crazy_level # removed cap of 6
            print("combat strength: " + str(hero.combat_strength))
            print("health points: " + str(hero.health_points))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        num_dream_lvls = -1
    print("num_dream_lvls: ", num_dream_lvls)

# --- Fight Sequence ---
print("    ------------------------------------------------------------------")
print("    |    You meet the monster. FIGHT!!")
monster.determine_behavior(hero)  # Show initial behavior

while hero.health_points > 0 and monster.health_points > 0:
    print("    |", end="    ")
    input("Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)

    if attack_roll % 2 != 0:
        print("    |", end="    ")
        input("You strike (Press Enter)")
        hero.attack(monster)
        if monster.health_points <= 0:
            num_stars = 3
        else:
            print("    |", end="    ")
            print("------------------------------------------------------------------")
            monster.attack(hero)
            if hero.health_points <= 0:
                num_stars = 1
            else:
                num_stars = 2
    else:
        print("    |", end="    ")
        monster.attack(hero)
        if hero.health_points <= 0:
            num_stars = 1
        else:
            print("    |", end="    ")
            print("------------------------------------------------------------------")
            input("The hero strikes!! (Press Enter)")
            hero.attack(monster)
            if monster.health_points <= 0:
                num_stars = 3
            else:
                num_stars = 2

if monster.health_points <= 0:
    winner = "Hero"
else:
    winner = "Monster"

# --- Final Score Display and Hero Name Input ---
tries = 0
input_invalid = True
while input_invalid and tries < 5:
    print("    |", end="    ")
    hero_name = input("Enter your Hero's name (in two words): ")
    name_parts = hero_name.split()
    if len(name_parts) != 2:
        print("    |    Please enter a name with two parts (separated by a space)")
        tries += 1
    else:
        if not (name_parts[0].isalpha() and name_parts[1].isalpha()):
            print("    |    Please enter an alphabetical name")
            tries += 1
        else:
            short_name = name_parts[0][:2] + name_parts[1][:1]
            print("    |    I'm going to call you " + short_name + " for short")
            input_invalid = False

if not input_invalid:
    stars_display = "*" * num_stars
    print("    |    Hero " + short_name + " gets <" + stars_display + "> stars")

    # --- Save Game Data ---
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            previous_kills = int(lines[0].strip()) if lines and lines[0].strip().isdigit() else 0
    except FileNotFoundError:
        previous_kills = 0

    if winner == "Hero":
        previous_kills += 1

    with open("save.txt", "w") as file:
        file.write(f"{previous_kills}\n")  # First line: kill count
        file.write(f"XP:{hero.level_system.xp}\n")  # Second line: XP
        file.write(f"LEVEL:{hero.level_system.level}\n")  # Third line: Level
        file.write(f"Won: {winner}\n")  # Fourth line: Winner
    print(f"    |    Game saved. Kills: {previous_kills} | Level: {hero.level_system.level}")