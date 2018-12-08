import random
from random import randint

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
        self.map = [[["-"] for _ in range(self.size)] for _ in range(self.size)]
        self.populate()

    def printmap(self):
        for y in self.map:
            for x in y:
                if str(x)[2:-2] == "-":
                    print(str(x)[2:-2], end=" ")
                else:
                    print(x[0].symbol, end=" ")
            print()

    def populate(self):
        for y in self.map:
            for x in y:
                if not bool(randint(0, roomclass.maxsize - self.size + 1)):
                    x[-1] = random.choice(monsters)


class monsterclass:
    def __init__(self, name, symbol, frequency=10):
        self.name = name
        self.symbol = symbol
        self.frequency = frequency


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


rooms = []
codes = []
monsters = [monsterclass("mongoloid", "M", 50),
            monsterclass("Skeleton", "S"),
            monsterclass("Pirate Skeleton", "P"),
            monsterclass("Living Corpse", "Z", 5)]
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
    code = input()
    while code not in codes:
        code = input()

    searchroombycode(code).printmap()
