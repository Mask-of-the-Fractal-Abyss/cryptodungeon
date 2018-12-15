import random


class boarditem:  # Super class for all objects that can be built/spawned on the map
    def __init__(self, name, symbol, flavor="This object has no flavor", attack=10, defense=3, inventory=None,
                 counter=1, health=10):
        if inventory is None:
            inventory = []
        self.health = health
        self.counter = counter
        self.inventory = inventory
        self.defense = defense
        self.attack = attack
        self.flavor = flavor
        self.symbol = symbol  # Symbol is the letter tht will represent them on the board
        self.name = name


class monsterclass(boarditem):  # Class for monsters which appear on the board
    def __init__(self, name, symbol, flavor="This object has no flavor", attack=10, defense=3,
                 inventory=None, counter=1, health=10):
        super().__init__(name, symbol, flavor, attack, defense, inventory, counter)
        self.health = health


class buildingclass(boarditem):  # Class for buildings on the board
    def __init__(self, name, symbol, flavor="This object has no flavor"):
        super().__init__(name, symbol, flavor)


class playerclass(boarditem):
    def __init__(self, name, symbol, room, flavor="", attack=10, defense=3, inventory=None, counter=1, health=10):
        super().__init__(name, symbol, flavor, attack, defense, inventory, counter, health)
        if inventory is None:
            inventory = []
        self.room = room


def newmonsterinstance():
    monsters = [["Mongoloid", "m", "The Mongoloid was once human, like yourself, but his form has been "
                                   "distorted by the dark magicks that dwell here.", 50],
                ["Skeleton", "s", "Battered bones: a dried, but not completely empty skeleton...", 10],
                ["Pirate Skeleton", "p",
                 "The pirate skeleton was lead into the darkness by his greed, "
                 "too bad it couldn't lead him out.", 10],
                ["Living Corpse", "z",
                 "Necromancy is not a joke, but this person used to think it was.",
                 5]]
    for monster in monsters.copy():
        for _ in range(monster[3]):
            monsters.append(monster)
    monster = random.choice(monsters)
    return monsterclass(monster[0], monster[1], monster[2])
