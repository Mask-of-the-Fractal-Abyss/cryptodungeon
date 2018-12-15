from random import randint
import pickle
import ast


def newline(line):
    with open("cryptodungeon.txt", "a") as crypt:
        crypt.write(str(line) + "\n")


def rewrite(lines):
    with open("cryptodungeon.txt", "w") as crypt:
        for line in lines:
            crypt.write(str(line) + "\n")


def getlines():
    with open("cryptodungeon.txt", "r") as crypt:
        return crypt.readlines()


def lineatindex(index):
    with open("cryptodungeon.txt", "r") as crypt:
        return crypt.readlines()[index]


def encrypttext(plaintext):
    cyphertext = ""
    for char in str(plaintext):
        cyphertext += str(ord(char)) + " "
    return cyphertext


def decrypttext(cyphertext):
    plaintext = ""
    for num in cyphertext.split():
        plaintext += str(chr(int(int(num))))
    return plaintext


def saveroomsandcodes(rooms, codes):
    encryptrooms = []
    for room in rooms:
        encryptrooms.append(pickle.dumps(room))
    newline(encrypttext(encryptrooms))
    newline(encrypttext(codes))
    newline(encrypttext())


def extractroomsandcodes():
    codes = list(ast.literal_eval(decrypttext(getlines()[-1])[1:-1]))
    rooms = list(ast.literal_eval(decrypttext(getlines()[-2])[1:-1]))
    for room in rooms:
        pickled = pickle.loads(room)
        rooms[rooms.index(room)] = pickled
    return rooms, codes
