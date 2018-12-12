import random
from random import randint
import items
import sys
import crypt
import pickle

print("You've just taken your first steps into a dark and deadly dungeon.  Thousands of rooms lie before you, waiting "
      "to be explored and conquered, \nbut this isn't a normal dungeon like you've encountered before, this is a "
      "Cryptodungeon...\n")

codelength = 2
percentrooms = 10
numberofcombos = 0
for i in range(codelength + 1):
    numberofcombos += 26 ** i
numberofrooms = numberofcombos / (100 / percentrooms)


class roomclass:
    maxsize = 11

    def __init__(self):
        self.code = generatecode()
        self.size = randint(3, roomclass.maxsize)
        self.map = mapclass([["-" for _ in range(self.size)] for _ in range(self.size)])
        self.map.populate()


class mapclass:  # Map class used for each room, 2D array
    def __init__(self, array):
        self.array = array
        self.size = len(array[0])

    def set(self, x, y, change):
        self.array[x][y] = change

    def get(self, x, y):
        return self.array[x][y]

    def swap(self, x1, y1, x2, y2):
        temp = self.array[x1][y1]
        self.array[x1][y1] = self.array[x2][y2]
        self.array[x2][y2] = temp

    def move(self, x, y, direction):
        print(x, y)
        if direction == "w":
            self.array[x - 1][y] = self.array[x][y]
            self.array[x][y] = "-"
        elif direction == "a":
            self.array[x][y - 1] = self.array[x][y]
            self.array[x][y] = "-"
        elif direction == "s":
            self.array[x + 1][y] = self.array[x][y]
            self.array[x][y] = "-"
        elif direction == "d":
            self.array[x][y + 1] = self.array[x][y]
            self.array[x][y] = "-"

    def printmap(self):  # Prints the 2D array
        print()
        for y in self.array:
            print("\n    ", end="")
            for x in y:
                if str(x) == "-":
                    print(str(x), end=" ")
                else:
                    print(x.symbol, end=" ")
        print("\n\n")

    def populate(self):  # Fills the 2D array with random monsters
        for y in self.array:
            for x in range(len(y)):
                if not bool(randint(0, roomclass.maxsize - self.size + 1)):
                    y[x] = random.choice(monsters)

    def searchfortype(self, searchtype):
        for y in self.array:
            for x in y:
                if type(x) == searchtype:
                    return x
        return None


class boarditem:  # Super class for all objects that can be built/spawned on the map
    def __init__(self, name, symbol, flavor="This object has no flavor", attack=10, defense=3, inventory=[], counter=1, health=10):
        self.health = health
        self.counter = counter
        self.inventory = inventory
        self.defense = defense
        self.attack = attack
        self.flavor = flavor
        self.symbol = symbol  # Symbol is the letter tht will represent them on the board
        self.name = name


class monsterclass(boarditem):  # Class for monsters which appear on the board
    def __init__(self, name, symbol, flavor="This object has no flavor", frequency=10, attack=10, defense=3, inventory=[], counter=1, health=10):
        super().__init__(name, symbol, flavor, attack, defense, inventory, counter, health)
        self.frequency = frequency


class buildingclass(boarditem):  # Class for buildings on the board
    def __init__(self, name, symbol, flavor="This object has no flavor"):
        super().__init__(name, symbol, flavor)


class playerclass(boarditem):
    def __init__(self, name, symbol, room, flavor="", attack=10, defense=3, inventory=[], counter=1, health=10):
        super().__init__(name, symbol, flavor, attack, defense, inventory, counter, health)
        self.room = room


def generatecode():
    letters = "abcdefghijklmnopqrstuvwxyz"
    code = ""
    for _ in range(codelength):
        code += random.choice(letters)
    return code


def searchroombycode(code):
    for r in rooms:
        if r.code == code:
            return r
    assert False, "CODE DOESN'T EXIST IN ROOMS"


def buildingnames():
    names = []
    for b in buildings:
        names.append(b.name)
    return names


def getcoords(item, arr):
    for y in arr:
        for x in y:
            if x == item:
                return y.index(x), arr.index(y)
    return None


def newgame():
    rooms = []
    codes = []
    for m in monsters.copy():
        for _ in range(m.frequency):
            monsters.append(m)

    while len(codes) <= numberofrooms:
        rooms.append(roomclass())
        codes.append(rooms[-1].code)
        if codes.count(codes[-1]) > 1:
            codes.pop(-1)
            rooms.pop(-1)
    return rooms, codes


monsters = [monsterclass("Mongoloid", "m", "The Mongoloid was once human, like yourself, but his form has been "
                                           "distorted by the dark magicks that dwell here.", 50),
            monsterclass("Skeleton", "s", "Battered bones: a dried, but not completely empty skeleton..."),
            monsterclass("Pirate Skeleton", "p", "The pirate skeleton was lead into the darkness by his greed, "
                                                 "too bad it couldn't lead him out."),
            monsterclass("Living Corpse", "z", "Necromancy is not a joke, but this person used to think it was.", 5)]
buildings = [buildingclass("Mine", "M"),
             buildingclass("Lantern", "L")]

if len(crypt.getlines()) == 0:
    totalplayers = int(input("You are the first to enter into this dungeon, how many total players will be entering "
                             "including yourself?"))
    rooms, codes = newgame()
    playername = input("Enter your name: ")
    playerflavor = input("Enter an optional flavor text for your character: ")
    player = playerclass(playername, playername.capitalize()[0], None, playerflavor)
else:
    rooms, codes = crypt.extractroomsandcodes()
    playername = input("Enter your name: ")
    found = 0
    for room in rooms:
        p = room.map.searchfortype(playerclass)
        if p is not None and p.name == playername:
            player = p
            found = 1
            break
    if found == 0:
        playerflavor = input("Enter an optional flavor text for your character: ")
        player = playerclass(playername, playername.capitalize()[0], None, playerflavor)

buildsbyname = lambda name: buildings[buildingnames().index(name)]
print("\nUse the search command to begin looking for unlockable rooms:\nSYNTAX: 'search <code>'\n\nMany commands can "
      "be abbreviated or typed in different ways, try 's <code>' or 'visit <code>'\n\n"
      "Use the help command to get a list of valid commands: \nSYNTAX: 'help'\n")
print(f"Here is your one free code, use it wisely: {codes[0]}")
while True:
    action = input("Enter a command: ").lower()
    try:
        command = action.split()[0]
    except:
        print("Enter a command.")
    if command in ["search", "s", "look", "find", "visit"]:
        try:
            code = action.split()[1]
        except:
            if player.room is not None:
                code = player.room.code
            else:
                print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <code>'")
        while code not in codes:
            code = input("Not found. Input a code to search: ").lower()
        if player.room is None and player.room != searchroombycode(code):
            room = searchroombycode(code)
            if player.room != room:
                if input("Code confirmed, enter room?") in ["yes", "y"]:
                    room.map.printmap()
                    startcoords = input("Type a pair of coordinates to enter the room at that spot").split()
                    try:
                        x = int(startcoords[0])
                        y = int(startcoords[1])
                        player.room = room
                        room.map.set(x, y, player)
                        room.map.printmap()
                    except:
                        print("Room canceled: Coordinates out of range")
        else:
            print("You cannot enter this room because you are already in a different room.")

    elif command in ["build", "b", "construct"]:
        try:
            code = action.split()[1]
        except:
            if player.room is not None:
                code = player.room.code
            else:
                print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <code>'")
        if code in codes:
            room = searchroombycode(code)
            room.map.printmap()
            coords = input("Coordinates for desired building in room?").lower().split()
            try:
                x = int(coords[0])
                y = int(coords[1])
                if room.map.get(x, y) == "-":
                    room.map.set(x, y, buildsbyname(input("Name of building?").capitalize()))
                    room.map.printmap()
                else:
                    print("There is already an object here.")
            except:
                print("Building canceled: Coordinates out of range, or building name not available")
        else:
            print("Build canceled")
    elif command in ["examine", "e"]:
        try:
            assert player.room is not None
            room = player.room
            x = int(action.split()[1])
            y = int(action.split()[2])
            room.map.printmap()
            try:
                selected = room.map.array[x][y]
                if selected != "-":
                    if type(selected) == playerclass:
                        print(selected.name)
                    print(selected.flavor)
                else:
                    print("Just an empty tile...")
            except:
                print("Coordinates out of range.")
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <coordinates>'\n- Make sure you are in a "
                  f"room before you use this command.\n")
    elif command in ["m", "move"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <direction (w, a, s, d)>'")
        if player.room is not None:
            try:
                x, y = getcoords(player, player.room.map.array)
                swap = {"w": lambda x, y: player.room.map.swap(x, y, x - 1, y),
                        "s": lambda x, y: player.room.map.swap(x, y, x + 1, y),
                        "a": lambda x, y: player.room.map.swap(x, y, x, y - 1),
                        "d": lambda x, y: player.room.map.swap(x, y, x, y + 1)}[code]
                # player.room.map.move(y, x, code)
                swap(y, x)
                player.room.map.printmap()
            except:
                print("input valid movement (w, a, s, d)")
        else:
            print("You must enter a room first")
    elif command in ["a", "attack"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <direction (w, a, s, d)>'")
        if player.room is not None:
            #try:
                x, y = getcoords(player, player.room.map.array)
                getcoordinates = {"w": lambda x, y: player.room.map.get(x - 1, y),
                             "s": lambda x, y: player.room.map.get(x + 1, y),
                             "a": lambda x, y: player.room.map.get(x, y - 1),
                             "d": lambda x, y: player.room.map.get(x, y + 1)}[code]
                subject = getcoordinates(y, x)
                if subject != "-":
                    subject.health -= player.attack - subject.defense
                    print(f"You dealt {player.attack - subject.defense} damage.")
                    print(f"{subject.name} has {subject.health} left.")
                    if subject.health < 1:
                        x, y = getcoords(subject, player.room.map.array)
                        player.room.map.set(y, x, "-")
                        print(f"\nYou destroyed {subject.name}")
                        player.room.map.printmap()
                    else:
                        player.health -= subject.counter
                        print(f"You took {subject.counter} damage.\nYour health is at {player.health}")
                        subject.counter += 1
                else:
                    print("You cannot attack an empty space.")
            #except:
            #    print("input valid direction (w, a, s, d)")
        else:
            print("You must enter a room first")

    elif command in ["stats"]:
        print(f"""
        HEALTH: {player.health}
        DEFENSE: {player.defense}
        ATTACK: {player.attack}
        COUNTER: {player.counter}
        EQUIPS: {player.inventory}
        """)
    elif command in ["l", "leave"]:
        x, y = getcoords(player, player.room.map.array)
        if x == 0 or x == len(player.room.map.array) - 1 or (y == 0 or y == len(player.room.map.array) - 1):
            player.room.map.set(y, x, "-")
            player.room = None
            print("You left the room")
        else:
            print("You must be on an edge square of a room to leave.")
    elif command in ["help", "h"]:
        print("""
        List of current implemented commands: 
        - ["search", "s", "look", "find", "visit"] <code>
        - ["build", "b", "construct"] <code>
        - ["examine", "e"] <coordinates>
        - ["m", "move"] <direction (w, a, s, d)>
        - ["stats"] prints your current health/attack/items etc.
        - ["l", "leave"]
        If you are in a room, you don\'t need to input a room code with the command.
        """)
    elif command == "exit":
        if player.room is None:
            print("Can't save: You are not in a room")
            break
        crypt.saveroomsandcodes(rooms, codes)
        print("Saved Successfully")
        break
print("\nGAME OVER:\nYou have been ENCRYPTED")
