import random
from random import randint
import datetime
from datetime import timedelta

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
        self.map = mapclass([[["-"] for _ in range(self.size)] for _ in range(self.size)])
        self.map.populate()


class mapclass:  # Map class used for each room, 2D array
    def __init__(self, array):
        self.array = array
        self.size = len(array[0])

    def set(self, x, y, change):
        self.array[x][y] = [change]

    def printmap(self):  # Prints the 2D array
        for y in self.array:
            for x in y:
                if str(x)[2:-2] == "-":
                    print(str(x)[2:-2], end=" ")
                else:
                    print(x[0].symbol, end=" ")
            print()

    def populate(self):  # Fills the 2D array with random monsters
        for y in self.array:
            for x in y:
                if not bool(randint(0, roomclass.maxsize - self.size + 1)):
                    x[-1] = random.choice(monsters)


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

print(codes[-1])
while True:
    action = input().lower()
    command = action.split()[0]
    if command in ["search", "s", "look", "find", "visit"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{action.split()[0]} <code>'")
        while code not in codes + ["q"]:
            code = input("Not found. Input a code to search, enter 'q' to stop searching: ").lower()
        searchroombycode(code).map.printmap()
    elif command in ["build", "b", "construct"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{action.split()[0]} <code>'")
        if code in codes:
            roommap = searchroombycode(code).map
            roommap.printmap()
            coords = input("Coordinates for desired building in room?").lower().split()
            try:
                x = int(coords[0])
                y = int(coords[1])
                roommap.set(x, y, buildsbyname(input("Name of building?").capitalize()))
                roommap.printmap()
            except:
                print("Building canceled: Coordinates out of range, or building name not available")
        else:
            print("Build canceled")
    elif command in ["inspect", "i", "information", "zoom"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{action.split()[0]} <code>'")
        if code in codes:
            roommap = searchroombycode(code).map
            roommap.printmap()
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
