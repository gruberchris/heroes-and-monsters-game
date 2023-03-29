import random

import emoji as emoji


class Monster:
    def __init__(self, name, health=0, damage=0, attack_chance=.0, special_attack_chance=.0):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_chance = attack_chance
        self.special_attack_chance = special_attack_chance
        self.min_damage = 1
        self.is_enraged = False
        self.health_cap = self.health
        self.is_rabid = False

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        if random.random() > self.attack_chance:
            return 0

        # Weapon attack
        total_damage = random.randint(self.min_damage, self.damage)
        print(emoji.emojize(f"The {self.name} attacks you with it's weapon, causing {total_damage} damage. :crossed_swords:"))

        # Rabid attack
        if self.is_rabid:
            rabid_damage = int(random.randint(self.min_damage, self.damage) * 1.5)
            total_damage += rabid_damage
            print(emoji.emojize(f"The {self.name} bites you, causing {rabid_damage} damage! :biohazard:"))

        # Special attack
        if random.random() <= self.special_attack_chance:
            total_damage += self._special_attack(other)

        # Subtract damage from the opponent's health
        other.health -= total_damage

        return total_damage

    def _special_attack(self, other):
        pass

    def heal(self, amount):
        self.health += amount

    def _becomes_rabid(self):
        self.is_rabid = True
        self.attack_chance = .9
        self.special_attack_chance = .3
        print(emoji.emojize(f"The {self.name} turns rabid! :biohazard:"))
        self.name = f"Rabid {self.name}"


class Goblin(Monster):
    def __init__(self):
        super(Goblin, self).__init__(name="Goblin", health=10, damage=2, attack_chance=.5, special_attack_chance=.6)

    def attack(self, other):
        rabid_chance = .4

        if random.random() <= rabid_chance and not self.is_rabid:
            self._becomes_rabid()

        return super(Goblin, self).attack(other)

    def _special_attack(self, other):
        special_attack_damage = random.randint(self.min_damage, self.damage)

        if self.is_rabid:
            special_attack_damage = int(special_attack_damage * 1.5)

        print(emoji.emojize(f"The {self.name} quickly thrusts a dagger into your chest, causing {special_attack_damage} damage. :face_with_spiral_eyes:"))

        return special_attack_damage


class Troll(Monster):
    def __init__(self):
        super(Troll, self).__init__(name="Troll", health=11, damage=2, attack_chance=.6, special_attack_chance=.5)

    def attack(self, other):
        health_regen_rate = random.randint(1, 2)

        if self.health < self.health_cap:
            heal_amount = min(health_regen_rate, self.health_cap - self.health)
            self.health += heal_amount
            print(emoji.emojize(f"The Troll regenerates {heal_amount} health! :red_heart:"))

        return super(Troll, self).attack(other)

    def _special_attack(self, other):
        special_attack_damage = random.randint(self.min_damage, self.damage)
        print(emoji.emojize(f"The Troll back hands you across your face, causing {special_attack_damage} damage. :face_with_spiral_eyes:"))
        return special_attack_damage


class Orc(Monster):
    def __init__(self):
        super(Orc, self).__init__(name="Orc", health=12, damage=2, attack_chance=.6, special_attack_chance=.3)

    def attack(self, other):
        return super(Orc, self).attack(other)

    def _special_attack(self, other):
        special_attack_damage = self.damage * 3
        print(emoji.emojize("The Orc does bonus triple damage to you! :face_screaming_in_fear:"))
        return special_attack_damage


class Vampire(Monster):
    def __init__(self):
        super(Vampire, self).__init__(name="Vampire", health=15, damage=3, attack_chance=.6, special_attack_chance=.5)

    def attack(self, other):
        return super(Vampire, self).attack(other)

    def _special_attack(self, other):
        special_attack_damage = self.damage
        heal_amount = self.damage

        if self.health < self.health_cap:
            heal_amount = min(heal_amount, self.health_cap - self.health)
            self.health += heal_amount
            print(emoji.emojize(f"The Vampire adds {heal_amount} to it's health! :red_heart:"))

        print(emoji.emojize("The Vampire grows stronger as your wounds open up! :face_screaming_in_fear:"))

        return special_attack_damage


class HillGiant(Monster):
    def __init__(self):
        super(HillGiant, self).__init__(name="Hill Giant", health=20, damage=4, attack_chance=.4, special_attack_chance=.05)

    def attack(self, other):
        if self.health <= self.health_cap * .3 and not self.is_enraged:
            self.is_enraged = True
            self.attack_chance = .9
            self.special_attack_chance = .15
            print(emoji.emojize("The Hill Giant is enraged! :enraged_face:"))
            self.name = "Enraged Hill Giant"

        return super(HillGiant, self).attack(other)

    def _special_attack(self, other):
        special_attack_damage = self.damage

        if self.is_enraged:
            special_attack_damage = int(self.damage * 1.5)

        print(emoji.emojize(f"The {self.name} smashes his fist into your face and does {special_attack_damage} bonus damage to you! :face_with_spiral_eyes:"))
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

        if other.is_enraged:
            attack_damage = attack_damage // 2

        other.health -= attack_damage

        return attack_damage

    def heal(self):
        # The hero can only heal up to half of their health cap
        healing_amount = random.randint(1, self.health_cap // 2)
        bonus_heal_amount = 0

        if random.random() <= self.bonus_healing_chance:
            bonus_heal_amount = random.randint(1, self.health_cap // 2)

        if self.health < self.health_cap:
            healing_amount = min(healing_amount + bonus_heal_amount, self.health_cap - self.health)
            self.health += healing_amount

            if bonus_heal_amount > 0:
                print(emoji.emojize(f"You healed yourself exceptionally well for {healing_amount} health! :red_heart: :red_heart:\n"))
            else:
                print(emoji.emojize(f"You healed yourself for {healing_amount} health! :red_heart:\n"))
        else:
            print(emoji.emojize("You have no wounds to heal. :confounded_face:\n"))

    def _special_attack(self, other):
        pass


class HeroesAndMonstersGame:
    def __init__(self):
        self.monsters = []
        self.monster = None
        self.hero = Hero(name="Hero", health=14, damage=5)

    def spawn_monsters(self, num_monsters):
        self.monsters = []
        for i in range(num_monsters):
            monster = random.choice([Goblin(), Troll(), Orc(), Vampire(), HillGiant()])
            self.monsters.append(monster)

    def get_next_monster(self):
        monster = random.choice(self.monsters)

        try:
            self.monsters.remove(monster)
        except ValueError:
            return None

        return monster

    def hero_attack(self):
        hero = self.hero
        monster = self.monster

        hero_attack_damage = hero.attack(monster)

        if hero_attack_damage > 0:
            if monster.is_enraged:
                print(emoji.emojize(f"You attack the {monster}, but your blows are reduced to {hero_attack_damage} damage by it's anger! :crossed_swords:\n"))
            else:
                print(emoji.emojize(f"You attack the {monster} and landed a cutting strike that did {hero_attack_damage} damage! :crossed_swords:\n"))
        else:
            print(emoji.emojize(f"You swing at, but miss striking the {monster}. :anguished_face:\n"))

        if not monster.is_alive():
            print(emoji.emojize(f"You killed the {monster}! :partying_face:\n"))
            self.monster = self.get_next_monster()
            hero.score += 1
            if self.monster is not None:
                appearance_message = self.get_monster_appears_message()
                print(appearance_message + "\n")

    def monster_attack(self):
        hero = self.hero
        monster = self.monster
        monster_damage = monster.attack(hero)

        if monster_damage:
            print()
        else:
            print(emoji.emojize(f"The {monster} attempts to strike you, but missed! :rolling_on_the_floor_laughing:\n"))

        if not hero.is_alive():
            print(emoji.emojize(f"The {monster} killed you! :wilted_flower:\n"))

    def get_monster_appears_message(self):
        monster = self.monster

        if type(self.monster) is Troll:
            return emoji.emojize(f"A {monster} has appeared! :troll:")
        elif type(self.monster) is Goblin:
            return emoji.emojize(f"A {monster} has appeared! :goblin:")
        elif type(self.monster) is Orc:
            return emoji.emojize(f"An {monster} has appeared! :ogre:")
        elif type(self.monster) is Vampire:
            return emoji.emojize(f"A {monster} has appeared! :vampire:")
        else:
            return f"A {monster} has appeared!"

    def main(self):
        print(emoji.emojize("Welcome to the Heroes & Monsters game. :skull:"))
        print(emoji.emojize("This land is dark and full of monsters. :waxing_crescent_moon:"))
        print(emoji.emojize("Who can say how many monsters you will encounter. :thinking_face:"))
        print(emoji.emojize("You are the hero and you must kill all the monsters. :crossed_swords:\n"))

        # Generate monsters
        monster_count = random.randint(3, 6)
        self.spawn_monsters(monster_count)

        # Spawn first monster
        self.monster = self.get_next_monster()
        monster_appears_message = self.get_monster_appears_message()
        print(monster_appears_message + "\n")

        while self.monster and self.hero.is_alive():
            self.hero.turns += 1
            print(f"You have {self.hero.health} health")
            print(f"The {self.monster} has {self.monster.health} health\n")
            print("What do you want to do?")
            print(f"1. Fight the {self.monster}")
            print("2. Heal yourself")
            print("3. Do nothing")
            print("4. Flee")
            print("> ", end=' ')

            try:
                selected_action = input()
            except KeyboardInterrupt:
                print("\n")
                break

            if selected_action == "1":
                self.hero_attack()
                if self.monster is not None:
                    self.monster_attack()
            elif selected_action == "2":
                self.hero.heal()
                self.monster_attack()
            elif selected_action == "3":
                self.monster_attack()
            elif selected_action == "4":
                break
            else:
                print(emoji.emojize(f"'{selected_action}' is not a valid choice. :confounded_face:\n"))

        if self.hero.is_alive() and len(self.monsters) == 0:
            print(emoji.emojize(f":trophy: You have killed all {self.hero.score} monsters and survived {self.hero.turns} turns! :trophy:"))
        elif self.hero.is_alive() and len(self.monsters) > 0:
            print(emoji.emojize(f"You run away from the monsters after surviving {self.hero.turns} turns. :person_running:"))
            print(emoji.emojize(":rooster: Coward! :hatching_chick:"))
        else:
            print(emoji.emojize(f"You survived {self.hero.turns} turns and slayed {self.hero.score} monsters, but now you meet your end. :skull:"))


if __name__ == "__main__":
    game = HeroesAndMonstersGame()
    game.main()
