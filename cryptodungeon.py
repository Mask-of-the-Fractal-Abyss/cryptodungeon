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


class mapclass:
    def __init__(self, array):
        self.array = array
        self.size = len(array[0])

    def set(self, x, y, change):
        self.array[x][y] = [change]

    def printmap(self):
        for y in self.array:
            for x in y:
                if str(x)[2:-2] == "-":
                    print(str(x)[2:-2], end=" ")
                else:
                    print(x[0].symbol, end=" ")
            print()

    def populate(self):
        for y in self.array:
            for x in y:
                if not bool(randint(0, roomclass.maxsize - self.size + 1)):
                    x[-1] = random.choice(monsters)


class boarditem:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class monsterclass(boarditem):
    def __init__(self, name, symbol, frequency=10):
        super().__init__(name, symbol)
        self.frequency = frequency


class buildingclass(boarditem):
    def __init__(self, constructiondelay, name, symbol):
        super().__init__(name, symbol)
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
monsters = [monsterclass("Mongoloid", "M", 50),
            monsterclass("Skeleton", "S"),
            monsterclass("Pirate Skeleton", "P"),
            monsterclass("Living Corpse", "Z", 5)]
buildings = [buildingclass("Mine", "M", timedelta(minutes=10)),
             buildingclass("Lantern", "L", timedelta(days=1))]
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
    if action.split()[0] in ["search", "s", "look", "find", "visit"]:
        try:
            code = action.split()[1]
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{action.split()[0]} <code>'")
        while code not in codes + ["q"]:
            code = input("Not found. Input a code to search, enter 'q' to stop searching: ").lower()
        searchroombycode(code).map.printmap()
    elif action.split()[0] in ["build", "b", "construct"]:
        code = action.split()[1]
        try:
            if code in codes:
                roommap = searchroombycode(code).map
                roommap.printmap()
                coords = input("Coordinates for desired building in room?").lower().split()
                x = int(coords[0])
                y = int(coords[1])
                try:
                    roommap.set(x, y, buildsbyname(input("Name of building?")))
                    roommap.printmap()
                except:
                    print("Coordinates out of range, or building name not available")
            else:
                print("Build canceled")
        except:
            print(f"\n\nEnter a code after the command.\nSYNTAX: '{action.split()[0]} <code>'")
