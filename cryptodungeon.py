import random
from random import randint

seed = "21004"
combos = 0
rooms = []

"""
for i in range(int(seed[0]) + 1):
    combos = combos + 26 ** i
"""


class room:
    def __init__(self, resources, size):

        self.code = generate_code()
        self.locked = True
        self.content = []

        for _ in range(size):
            self.content.append(0)

        for _ in range(resources):
            self.content[randint(0, len(self.content) - 1)] += 1

    def unlock(self, code):
        if code == self.code:
            self.locked = False
            print("Unlocked!")
        else:
            print("Wrong code!")

    def view(self):
        if not self.locked:
            return (self.content)
        else:
            print("Room is locked!")


def save_rooms(file):
    for room in rooms:
        pass


def generate_code():
    stuff = "abcdefghijklmnopqrstuvwxyz"
    code = ""
    for _ in range(int(seed[0]) + 1):
        code = code + random.choice(stuff)
    return code


def generate_rooms(n):
    for _ in range(n):
        rooms.append(room(randint(0, int(seed[4])), randint(1, (int(seed[4]) + 1))))


def crack_lock(room):
    while rooms[0].locked:
        code = generate_code()
        print(code)
        rooms[0].unlock(code)


generate_rooms(5)

# try rooms[0].view()
# then crack_lock(rooms[0])
# then again rooms[0].view()










