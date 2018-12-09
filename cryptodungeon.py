import random
from random import randint
import datetime
from datetime import timedelta
import sys

print("You've just taken your first steps into a dark and deadly dungeon.  Thousands of rooms lie before you, waiting "
      "to be explored and conquered, \nbut this isn't a normal dungeon like you've encountered before, this is a "
      "Cryptodungeon...\n")

timestart = datetime.datetime.now()
codelength = 3
percentrooms = 10
numberofcombos = 0
for i in range(codelength + 1):
    numberofcombos += 26 ** i
numberofrooms = numberofcombos / (100 / percentrooms)


class roomclass:
    maxsize = 7

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

    def swap(self, x1, y1, x2, y2):
        temp = self.array[x1][y1]
        self.array[x1][y1] = self.array[x2][y2]
        self.array[x2][y2] = temp

    def printmap(self):  # Prints the 2D array
        for y in self.array:
            for x in y:
                if str(x) == "-":
                    print(str(x), end=" ")
                else:
                    print(x.symbol, end=" ")
            print()

    def populate(self):  # Fills the 2D array with random monsters
        for y in self.array:
            for x in range(len(y)):
                if not bool(randint(0, roomclass.maxsize - self.size + 1)):
                    y[x] = random.choice(monsters)


class boarditem:  # Super class for all objects that can be built/spawned on the map
    def __init__(self, name, symbol, flavor="This object has no flavor"):
        self.name = name
        self.symbol = symbol  # Symbol is the letter tht will represent them on the board
        self.flavor = flavor


class monsterclass(boarditem):  # Class for monsters which appear on the board
    def __init__(self, name, symbol, flavor="This object has no flavor", frequency=10):
        super().__init__(name, symbol, flavor)
        self.frequency = frequency


class buildingclass(boarditem):  # Class for buildings on the board
    def __init__(self, constructiondelay, name, symbol, flavor="This object has no flavor"):
        super().__init__(name, symbol, flavor)
        self.constructiondelay = constructiondelay


class playerclass(boarditem):
    def __init__(self, name, symbol, room):
        super().__init__(name, symbol)
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


rooms = []
codes = []
monsters = [monsterclass("Mongoloid", "m", "The Mongoloid was once human, like yourself, but his form has been "
                                           "distored by the dark magicks that dwell here.", 50),
            monsterclass("Skeleton", "s", "Battered bones: a dried, but not completely empty skeleton..."),
            monsterclass("Pirate Skeleton", "p", "The pirate skeleton was lead into the darkness by his greed, "
                                                 "too bad it couldn't lead him out."),
            monsterclass("Living Corpse", "z", "Necromancy is not a joke, but this person used to think it was.", 5)]
buildings = [buildingclass(timedelta(minutes=10), "Mine", "M"),
             buildingclass(timedelta(days=1), "Lantern", "L")]
buildsbyname = lambda name: buildings[buildingnames().index(name)]
for m in monsters.copy():
    for _ in range(m.frequency):
        monsters.append(m)

while len(codes) <= numberofrooms:
    rooms.append(roomclass())
    codes.append(rooms[-1].code)
    if codes.count(codes[-1]) > 1:
        codes.pop(-1)
        rooms.pop(-1)

player = playerclass(input("Enter your name: "), "@", None)
print("Use the search command to begin looking for unlockable rooms:\nSYNTAX: 'search <code>'\n\nMany commands can be "
      "abbreviated or typed in different ways, try 's <code>' or 'visit <code>'\n\n"
      "Use the help command to get a list of valid commands: \nSYNTAX: 'help'")
print(f"Here is your one free code, use it wisely: {random.choice(codes)}")
while True:
    action = input().lower()
    command = action.split()[0]
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
                room.map.set(x, y, buildsbyname(input("Name of building?").capitalize()))
                room.map.printmap()
            except:
                print("Building canceled: Coordinates out of range, or building name not available")
        else:
            print("Build canceled")
    elif command in ["inspect", "i", "information", "zoom"]:
        try:
            code = action.split()[1]
        except:
            if player.room is not None:
                code = player.room.code
            else:
                print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <code>'")
        if code in codes:
            room.map = searchroombycode(code).map
            room.map.printmap()
            coords = input("Coordinates in room to inspect?").lower().split()
            try:
                x = int(coords[0])
                y = int(coords[1])
                if roommap.array[x][y][0] != "-":
                    print(roommap.array[x][y][0].flavor)
                else:
                    print("Just an empty tile...")
            except:
                print("Coordinates out of range.")
    elif command in ["m", "move"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{command} <direction (w, a, s, d)>'")
        if player.room is not None:
            try:
                x, y = getcoords(player, player.room.map.array)
                code = {"w": lambda x, y: player.room.map.swap(x, y, x - 1, y),
                        "s": lambda x, y: player.room.map.swap(x, y, x + 1, y),
                        "a": lambda x, y: player.room.map.swap(x, y, x, y - 1),
                        "d": lambda x, y: player.room.map.swap(x, y, x, y + 1)}[code]
                code(y, x)
                player.room.map.printmap()
            except:
                print("input valid movement (w, a, s, d)")
        else:
            print("You must enter a room first")
    elif command in ["l", "leave"]:
        x, y = getcoords(player, player.room.map.array)
        if x == 0 or x == len(player.room.map.array) - 1 or (y == 0 or y == len(player.room.map.array) - 1):
            player.room.map.set(y, x, "-")
            player.room = None
            print("You left the room")
        else:
            print("You must be on an edge square of a room to leave.")
