import random

import emoji as emoji


class Monster:
    def __init__(self, name, health, damage, attack_chance, special_attack_chance):
        self.name = name
        self.health = health
        self.damage = damage
        self.min_damage = 1
        self.attack_chance = attack_chance
        self.special_attack_chance = special_attack_chance

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        if random.random() > self.attack_chance:
            return 0

        total_damage = random.randint(self.min_damage, self.damage)

        if random.random() <= self.special_attack_chance:
            total_damage += self.special_attack(other)

        other.health -= total_damage

        return total_damage

    def special_attack(self, other):
        pass

    def heal(self, amount):
        self.health += amount


class Goblin(Monster):
    def __init__(self):
        super(Goblin, self).__init__(name="Goblin", health=8, damage=2, attack_chance=.5, special_attack_chance=.6)

    def attack(self, other):
        return super(Goblin, self).attack(other)

    def special_attack(self, other):
        special_attack_damage = self.damage * 2
        print(emoji.emojize("The Goblin does bonus double damage to you! :face_with_spiral_eyes:"))
        return special_attack_damage


class Troll(Monster):
    def __init__(self):
        super(Troll, self).__init__(name="Troll", health=10, damage=1, attack_chance=.8, special_attack_chance=.5)
        self.health_cap = self.health

    def attack(self, other):
        health_regen_rate = random.randint(1, 2)

        if self.health < self.health_cap:
            heal_amount = min(health_regen_rate, self.health_cap - self.health)
            self.health += heal_amount
            print(emoji.emojize("The Troll regenerates {} health! :red_heart:").format(heal_amount))

        return super(Troll, self).attack(other)

    def special_attack(self, other):
        special_attack_damage = random.randint(1, 3)
        emoji_message = emoji.emojize("The Troll does {} bonus damage to you! :pile_of_poo:")
        print(emoji_message.format(special_attack_damage))
        return special_attack_damage


class Orc(Monster):
    def __init__(self):
        super(Orc, self).__init__(name="Orc", health=12, damage=2, attack_chance=.6, special_attack_chance=.3)

    def attack(self, other):
        return super(Orc, self).attack(other)

    def special_attack(self, other):
        special_attack_damage = self.damage * 3
        print(emoji.emojize("The Orc does bonus triple damage to you! :face_screaming_in_fear:"))
        return special_attack_damage


class Vampire(Monster):
    def __init__(self):
        super(Vampire, self).__init__(name="Vampire", health=15, damage=3, attack_chance=.6, special_attack_chance=.5)
        self.health_cap = self.health

    def attack(self, other):
        return super(Vampire, self).attack(other)

    def special_attack(self, other):
        special_attack_damage = self.damage
        heal_amount = self.damage

        if self.health < self.health_cap:
            heal_amount = min(heal_amount, self.health_cap - self.health)
            self.health += heal_amount
            print(emoji.emojize("The Vampire adds {} to it's health! :red_heart:").format(heal_amount))

        print(emoji.emojize("The Vampire grows stronger as your wounds open up! :face_screaming_in_fear:"))

        return special_attack_damage


class Hero:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        self.health_cap = health
        self.attack_chance = .8
        self.score = 0
        self.turns = -1
        self.bonus_healing_chance = .3

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        attack_damage = random.randint(1, self.damage)

        if random.random() > self.attack_chance:
            return 0

        other.health -= attack_damage

        return attack_damage

    def heal(self):
        # The hero can only heal up to half of their health cap
        healing_amount = random.randint(1, self.health_cap // 2)
        bonus_heal_amount = 0

        if random.random() <= bonus_heal_amount:
            bonus_heal_amount = random.randint(1, self.health_cap // 2)

        if self.health < self.health_cap:
            heal_amount = min(healing_amount + bonus_heal_amount, self.health_cap - self.health)
            self.health += heal_amount

            if bonus_heal_amount > 0:
                print(emoji.emojize("You healed yourself exceptionally well for {} health! :red_heart: :red_heart:\n").format(heal_amount))
            else:
                print(emoji.emojize("You healed yourself for {} health! :red_heart:\n").format(healing_amount))
        else:
            print(emoji.emojize("You have no wounds to heal. :confounded_face:\n"))

    def _special_attack(self, other):
        pass


class HeroesAndMonstersGame:
    def __init__(self):
        self.monsters = [Goblin(), Troll(), Orc(), Vampire()]
        self.monster = self.get_next_monster()
        self.hero = Hero(name="Hero", health=14, damage=5)

    def spawn_monsters(self, num_monsters):
        self.monsters = []
        for i in range(num_monsters):
            monster = random.choice([Goblin(), Troll(), Orc()])
            self.monsters.append(monster)

    def get_next_monster(self):
        try:
            monster = random.choice(self.monsters)
            self.monsters.remove(monster)
            return monster
        except IndexError:
            return None

    def hero_attack(self):
        hero = self.hero
        monster = self.monster

        hero_attack_damage = hero.attack(monster)

        if hero_attack_damage > 0:
            print(emoji.emojize(
                "You attack the {} and landed a mighty blow that did {} damage! :crossed_swords:\n").format(monster,
                                                                                                            hero_attack_damage))
        else:
            print(emoji.emojize("You swing, but missed striking the {}. :anguished_face:\n").format(monster))

        if not monster.is_alive():
            print(emoji.emojize("You killed the {}! :partying_face:\n").format(monster))
            self.monster = self.get_next_monster()
            hero.score += 1
            if self.monster is not None:
                appearance_message = self.get_monster_appears_message()
                print(appearance_message + "\n")

    def monster_attack(self):
        hero = self.hero
        monster = self.monster

        monster_damage = monster.attack(hero)

        if monster_damage > 0:
            print(emoji.emojize("The {} attacks you and does {} damage! :crossed_swords:\n").format(monster,
                                                                                                    monster_damage))
        else:
            print(emoji.emojize("The {} attempts to strike you, but missed! :rolling_on_the_floor_laughing:\n").format(
                monster))

        if not hero.is_alive():
            print(emoji.emojize("The {} killed you! :wilted_flower:\n".format(monster)))

    def get_monster_appears_message(self):
        if type(self.monster) is Troll:
            return emoji.emojize("A {} has appeared! :troll:").format(self.monster)
        elif type(self.monster) is Goblin:
            return emoji.emojize("A {} has appeared! :goblin:").format(self.monster)
        elif type(self.monster) is Orc:
            return emoji.emojize("An {} has appeared! :ogre:").format(self.monster)
        else:
            return "A {} has appeared!".format(self.monster)

    def main(self):
        print(emoji.emojize("Welcome to the Heroes & Monsters game. :skull:"))
        print(emoji.emojize("This land is dark and full of monsters. :waxing_crescent_moon:"))
        print(emoji.emojize("Who can say how many monsters you will encounter. :thinking_face:"))
        print(emoji.emojize("You are the hero and you must kill all the monsters. :crossed_swords:\n"))

        monster_count = random.randint(3, 6)
        self.spawn_monsters(monster_count)
        monster_appears_message = self.get_monster_appears_message()
        print(monster_appears_message + "\n")

        while self.monster and self.hero.is_alive():
            self.hero.turns += 1
            print("You have {} health".format(self.hero.health))
            print("The {} has {} health\n".format(self.monster, self.monster.health))
            print("What do you want to do?")
            print("1. Fight the {}".format(self.monster))
            print("2. Heal yourself")
            print("3. Do nothing")
            print("4. Flee")
            print("> ", end=' ')

            try:
                raw_input = input()
            except KeyboardInterrupt:
                print("\n")
                break

            if raw_input == "1":
                self.hero_attack()
                if self.monster is not None:
                    self.monster_attack()
            elif raw_input == "2":
                self.hero.heal()
                self.monster_attack()
            elif raw_input == "3":
                self.monster_attack()
            elif raw_input == "4":
                break
            else:
                print("Invalid choice {}".format(raw_input))

        if self.hero.is_alive() and len(self.monsters) == 0:
            print(emoji.emojize(":trophy: You have killed all {} monsters and survived {} turns! :trophy:").format(
                self.hero.score, self.hero.turns))
            print(emoji.emojize(":partying_face: Good job! :partying_face:"))
        elif self.hero.is_alive() and len(self.monsters) > 0:
            print(emoji.emojize("You run away from the monsters after surviving {} turns. :person_running:").format(
                self.hero.turns))
            print(emoji.emojize(":rooster: Coward! :hatching_chick:"))
        else:
            print(emoji.emojize(
                "You survived {} turns and slayed {} monster, but this is where your adventure ends.").format(
                self.hero.turns, self.hero.score))
            print(emoji.emojize(":skull: Game over. :skull:"))


if __name__ == "__main__":
    game = HeroesAndMonstersGame()
    game.main()
