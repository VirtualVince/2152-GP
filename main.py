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
hero.combat_strength = cs
monster.combat_strength = mcs

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
# Adjust hero's combat strength based on weapon roll (max remains 6)
hero.combat_strength = min(6, hero.combat_strength + weapon_roll)
print("    |    The hero's weapon is " + str(weapons[weapon_roll - 1]))

# --- Adjust Combat Strength Based on Previous Game ---
def load_previous_game():
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()
    except FileNotFoundError:
        return None

last_game = load_previous_game()
if last_game:
    if "Hero" in last_game and "gained" in last_game:
        print("    |    ... Increasing the monster's combat strength since you won so easily last time")
        monster.combat_strength = min(6, monster.combat_strength + 1)
    elif "Monster" in last_game:
        print("    |    ... Increasing the hero's combat strength since you lost last time")
        hero.combat_strength = min(6, hero.combat_strength + 1)
    else:
        print("    |    ... No changes in combat strength based on previous game.")

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
monster.combat_strength = min(6, monster.combat_strength + monster_powers[power_roll])
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
            hero.combat_strength = min(6, hero.combat_strength + crazy_level)
            print("combat strength: " + str(hero.combat_strength))
            print("health points: " + str(hero.health_points))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        num_dream_lvls = -1
    print("num_dream_lvls: ", num_dream_lvls)


# --- Fight Sequence ---
print("    ------------------------------------------------------------------")
print("    |    You meet the monster. FIGHT!!")
while hero.health_points > 0 and monster.health_points > 0:
    print("    |", end="    ")
    input("Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)

    if attack_roll % 2 != 0:
        print("    |", end="    ")
        input("You strike (Press Enter)")
        hero.attack(monster)

        if monster.health_points <= 0:
            if hero.health_points == 20:
                num_stars = 4
                print("    |    Perfect combo! Hero defeated the monster without taking damage.")
            else:
                num_stars = 3
            break
        else:
            print("    |", end="    ")
            print("------------------------------------------------------------------")
            input("    |    The monster strikes (Press Enter)!!!")
            monster.attack(hero)

            if hero.health_points <= 0:
                num_stars = 1
                break
            else:
                num_stars = 2
    else:
        print("    |", end="    ")
        input("The Monster strikes (Press Enter)")
        monster.attack(hero)

        if hero.health_points <= 0:
            num_stars = 1
            break
        else:
            print("    |", end="    ")
            print("------------------------------------------------------------------")
            input("The hero strikes!! (Press Enter)")
            hero.attack(monster)

            if monster.health_points <= 0:
                if hero.health_points == 20:
                    num_stars = 4
                    print("    |    Perfect combo! Hero defeated the monster without taking damage.")
                else:
                    num_stars = 3
                break
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
            previous = file.readline().strip()
            previous_kills = int(previous) if previous.isdigit() else 0
    except FileNotFoundError:
        previous_kills = 0

    if winner == "Hero":
        previous_kills += 1

    with open("save.txt", "w") as file:
        file.write(str(previous_kills))
    print("    |    Game saved. Total monsters defeated across games: " + str(previous_kills))
