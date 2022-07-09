# Purpose: Simulate a text adventure
# Author: Gazel
# Date: October 14th, 2019
import random


# A generic class for holding a weapon's name and damage stat
class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


# A generic class for holding an armor item's type (helmet, chesplate, leggings, helmet), name, and defense stat
class Armor:
    def __init__(self, type, name, defense):
        self.type = type
        self.name = name
        self.defense = defense


# A generic class for holding a player object which has hp, a weapon, 4 armor pieces, and a room counter
class Player:
    def __init__(self, hit_points, weapon, armor_dict, room_counter):
        self.max_hit_points = hit_points
        self.current_hit_points = hit_points
        self.weapon = weapon
        self.armor_dict = armor_dict
        self.armor_rating = 0
        self.room_counter = room_counter
        self.update_armor_rating()

    # Armor rating, used to calculate damage. Updated here since no "setter" and "getter" methods exist
    def update_armor_rating(self):
        self.armor_rating = 0
        self.armor_rating += self.armor_dict["Helmet"].defense
        self.armor_rating += self.armor_dict["Chestplate"].defense
        self.armor_rating += self.armor_dict["Leggings"].defense
        self.armor_rating += self.armor_dict["Boots"].defense


# Simulates a random event given a player object
def random_event(player):
    methods = {0: find_item, 1: monster_encounter}
    method = methods[random.randrange(0, 2)]
    return method(player)


# Monster Encounter Event
def monster_encounter(player):
    level_list = {9: "Weak", 10: "Normal", 11: "Strong", 12: "Powerful", 13: "Epic", 14: "Legendary", 15: "Satanic"}
    monster_type_list = {0: "Flea", 1: "Rat", 2: "Skeleton", 3: "Zombie", 4: "Vampire",
                         5: "Werewolf", 6: "Golem", 7: "Dragon", 8: "Demon"}
    monster_hit_points_list = {0: 6, 1: 8, 2: 9, 3: 9, 4: 10, 5: 11, 6: 12, 7: 14, 8: 18}

    monster_damage = random.randrange(9, len(
        level_list) + 9)  # Damage is a random number that exists in the level_lists dictionary
    monster_level = level_list[monster_damage]  # Monster level (weak, legendary) correlates to the monster's damage
    temp_rand = random.randrange(len(monster_type_list))
    monster_type = monster_type_list[temp_rand]  # Random monster type (Flea, Skeleton, Dragon)
    monster_max_hit_points = monster_hit_points_list[temp_rand]  # Hitpoints are based on the monster's type
    monster_current_hit_points = monster_max_hit_points  # Current hit points is set to help with later math

    monster_name = monster_level + " " + monster_type  # Makes printing easier

    battle_end = False

    print("You encounter a " + monster_name + " with " + str(monster_max_hit_points) + " HP.")
    input("You encounter a " + monster_name + " with " + str(monster_max_hit_points) + " HP. Continue:")

    monster_net_damage = monster_damage - player.armor_rating

    # Battle sequence, lasts until monster dead, player dead, or player escape
    while monster_current_hit_points > 0 and player.current_hit_points > 0 and not battle_end:

        # Player input faze, attack or run
        player_choice = "z"
        while player_choice != "a" and player_choice != "r":
            try:
                player_choice = input("The " + monster_name + " has " + str(monster_current_hit_points) + "/" +
                                      str(monster_max_hit_points) + " HP." +
                                      " You have " + str(player.current_hit_points) + "/" +
                                      str(player.max_hit_points) + " HP. "
                                                                   "Do you attack or run (a or r)? ")
            except TypeError:
                pass

        # If attacking, run player attack and then monster attack
        if player_choice == "a":

            # Player attack and end if monster dies
            if monster_current_hit_points - player.weapon.damage > 0:
                monster_current_hit_points -= player.weapon.damage
                print("You deal " + str(player.weapon.damage) + " damage and the monster now has " +
                      str(monster_current_hit_points) + "/" + str(monster_max_hit_points) + " HP.")
                input("You deal " + str(player.weapon.damage) + " damage and the monster now has " +
                      str(monster_current_hit_points) + "/" + str(monster_max_hit_points) + " HP. Continue: ")
            else:
                monster_current_hit_points -= player.weapon.damage
                print("You deal " + str(player.weapon.damage) + " damage and the " + monster_name + " is now dead.")
                input("You deal " + str(player.weapon.damage) + " damage and the " + monster_name +
                      " is now dead. Continue: ")
                break

            # Monster attack - player's defense, end if player dies
            if player.armor_rating - monster_damage >= 0:
                print("The " + monster_name + " is too weak to hurt you.")
                input("The " + monster_name + " is too weak to hurt you. Continue: ")
            elif player.current_hit_points + player.armor_rating - monster_damage > 0:
                player.current_hit_points += player.armor_rating - monster_damage

                print("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                      str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP.")
                input("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                      str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP. Continue: ")
            else:
                player.current_hit_points = 0
                print("The " + monster_name + " dealt " + str(monster_net_damage) + " damage and you now have " +
                      str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP.")
                print("You are dead.")
                input("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                      str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP. You are dead.")

        # Running has a higher chance the earlier the floor and will always be successful if player can't take damage
        if player_choice == "r":
            if random.randrange(80 + int(player.room_counter / 2.0)) <= 65 or player.armor_rating - monster_damage >= 0:
                print("You successfully escape!")
                input("You successfully escape! Continue:")
                battle_end = True
            else:
                monster_net_damage = monster_damage - player.armor_rating
                if player.current_hit_points - monster_damage > 0:
                    player.current_hit_points -= monster_damage
                    print("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                          str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP.")
                    input("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                          str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP. Continue: ")
                else:
                    player.current_hit_points = 0
                    print("The " + monster_name + " dealt " + str(monster_net_damage) + " damage and you now have " +
                          str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP.")
                    print("You are dead.")
                    input("The " + monster_name + " deals " + str(monster_net_damage) + " damage and you now have " +
                          str(player.current_hit_points) + "/" + str(player.max_hit_points) + " HP. You are dead.")


# Allows the player to get better gear and heal
def find_item(player):
    item_methods = {0: find_weapon, 1: find_armor, 2: find_health}

    # Can't find a potion if at max hp
    if player.current_hit_points < player.max_hit_points:
        num = random.randrange(0, 3)
    else:
        num = random.randrange(0, 2)

    method = item_methods[num]
    level_modifier = {4: "Small", 5: "Average", 6: "Large", 7: "Epic", 8: "Legendary", 9: "Godly"}
    material_modifier = {0: "Copper", 1: "Tin", 2: "Bronze", 3: "Gold", 4: "Steel", 5: "Iron", 6: "Titanium"}

    # Found weapon
    if num < 2:
        level = random.randrange(4, len(level_modifier) + 4)  # Damage/defense based on keys of level_modifier
        # dictionary
        level_name = level_modifier[level]  # Name is based on the damage/defense
        material = material_modifier[random.randrange(0, len(material_modifier))]  # Material is random flavor text

        switch_answer = "z"  # Initializing variable to avoid error

        # Weapon find
        if num == 0:
            name = level_name + " " + material + " " + method()
            found_weapon = Weapon(name, level)

            print("You found a " + found_weapon.name + " that does " + str(found_weapon.damage) + " damage." +
                  " Your current weapon is a " + player.weapon.name + " and does " + str(
                player.weapon.damage) + " damage.")

            # Input if pickup
            while True:  # switch_answer != "y" or switch_answer != "n"
                try:
                    switch_answer = str(input("You found a " + found_weapon.name + " that does " +
                                              str(found_weapon.damage) + " damage." +
                                              " Your current weapon is a " + player.weapon.name + " and does " +
                                              str(player.weapon.damage) + " damage." +
                                              " Would you like to switch (y or n): ").lower())
                except TypeError:
                    pass
                finally:
                    if switch_answer == "y" or switch_answer == "n":
                        break

            # Execute if picked up
            if switch_answer == "y":
                player.weapon = found_weapon
                print("Weapons swapped.")
            elif switch_answer == "n":
                print("Weapon left.")
            else:
                raise TypeError("Expected variable to be y or n, was " + str(switch_answer))

        # Armor Find
        if num == 1:
            level = int(level / 2)
            armor_type = method()
            name = level_name + " " + material + " " + armor_type
            found_armor = Armor(armor_type, name, level)

            print("You found a/some " + found_armor.name + " that have/has " + str(found_armor.defense) + " defense." +
                  " Your current " + found_armor.type + " is/are called " + player.armor_dict[armor_type].name +
                  " and have/has " + str(player.armor_dict[armor_type].defense) + " defense.")

            # Input if pickup
            while True:  # switch_answer != "y" or switch_answer != "n"
                try:
                    switch_answer = str(input(
                        "You found a/some " + found_armor.name + " that have/has " + str(found_armor.defense) +
                        " defense." +
                        " Your current " + armor_type + " is/are called " +
                        player.armor_dict[armor_type].name + " and have/has " +
                        str(player.armor_dict[armor_type].defense) + " defense." +
                        " Would you like to switch (y or n): ").lower())
                except TypeError:
                    pass
                finally:
                    if switch_answer == "y" or switch_answer == "n":
                        break

            # Execute if picked up
            if switch_answer == "y":
                player.armor_dict[armor_type] = found_armor
                player.update_armor_rating()
                print("Armor swapped. new armor rating is " + str(player.armor_rating) + ".")
                input("New armor rating is " + str(player.armor_rating) + ".")
            elif switch_answer == "n":
                print("Armor left.")
            else:
                raise TypeError("Expected variable to be y or n, was " + str(switch_answer))

    # Potion found
    elif num == 2:
        old_hp = str(player.current_hit_points)
        potion_health = find_health(player.max_hit_points)

        # Heals, if hp added is > max hp, just set to max
        if player.current_hit_points + potion_health > player.max_hit_points:
            player.current_hit_points = player.max_hit_points
        else:
            player.current_hit_points += potion_health

        print("HP was " + str(old_hp) + "/" + str(player.max_hit_points) + ". Found a " + str(
            potion_health) + "hp potion." +
              " Now HP is " + str(player.current_hit_points) + "/" + str(player.max_hit_points) + ".")
        input("HP was " + str(old_hp) + "/" + str(player.max_hit_points) + ". Found a " + str(
            potion_health) + "hp potion." +
              " Now HP is " + str(player.current_hit_points) + "/" + str(player.max_hit_points) + "." +
              " Continue:")


# Returns a weapon name
def find_weapon():
    weapon_list = {0: "BattleAxe", 1: "Rapier", 2: "Cleaver", 3: "BroadSword", 4: "Mace"}
    return weapon_list[random.randrange(len(weapon_list))]


# Returns an armor name
def find_armor():
    armor_list = {0: "Helmet", 1: "Chestplate", 2: "Leggings", 3: "Boots"}
    return armor_list[random.randrange(len(armor_list))]


# Returns an random number based on max hp given in
def find_health(max_hp):
    max_potion_value = int(max_hp / 2)
    min_potion_value = int(max_hp / 4)
    return random.randrange(min_potion_value, max_potion_value)


# Where the game "takes place"
def main():
    print("============================" +
          "\nWelcome to The Death Dungeon" +
          "\n============================")
    counter = 1
    hp = 25
    weapon = Weapon("Stick", 2)
    armor_dict = {"Helmet": Armor("Helmet", "Baseball Cap", 1),
                  "Chestplate": Armor("Chestplate", "Tarnished T-Shirt", 1),
                  "Leggings": Armor("Leggings", "Ripped Jeans", 1),
                  "Boots": Armor("Boots", "Rain Boots", 1)}

    # Making player object
    player = Player(hp, weapon, armor_dict, counter)

    # While the player isn't dead keep going
    while player.current_hit_points > 0:
        print("You enter room #" + str(player.room_counter) + ".")
        input("You enter room #" + str(player.room_counter) + ". Continue:")

        # Three events per room
        for i in range(3):
            random_event(player)
            if player.current_hit_points <= 0:
                break

        # Used to determine run chance and give game over message
        player.room_counter += 1

    print("You survived for " + str(player.room_counter) + " rooms. Game Over.")


main()