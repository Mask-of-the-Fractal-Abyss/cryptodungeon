import random
from random import randint

codelength = 3
numberofcombos = 0
for i in range(codelength):
    numberofcombos += 26 ** i
numberofrooms = numberofcombos


class roomclass:
    maxroomsize = 10

    def __init__(self):
        self.code = generatecode()
        self.size = randint(1, 10)
        self.map = [[[] for _ in range(self.size)] for _ in range(self.size)]

    def printmap(self):
        for y in self.map:
            for x in y:
                print(x, end=" ")
            print()


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
while len(codes) <= numberofrooms:
    rooms.append(roomclass())
    codes.append(rooms[-1].code)
    if codes.count(codes[-1]) > 1:
        codes.pop(-1)
        rooms.pop(-1)

print(codes[-1])
while input() not in codes:
    pass

code = input("REINPUT CODE")
searchroombycode(code).printmap()