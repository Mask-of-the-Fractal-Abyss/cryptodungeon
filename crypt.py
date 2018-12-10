from random import randint
import pickle


def newline(line):
    with open("cryptodungeon.txt", "a") as crypt:
        crypt.write(str(line) + "\n")


def getlines():
    with open("cryptodungeon.txt", "r") as crypt:
        return crypt.readlines()


def lineatindex(index):
    with open("cryptodungeon.txt", "r") as crypt:
        return crypt.readlines()[index]


def encrypttext(plaintext, key=1):
    cyphertext = ""
    for char in str(plaintext):
        cyphertext += str(ord(char) * key) + " "
    return cyphertext


def decrypttext(cyphertext, key=1):
    plaintext = ""
    for num in cyphertext.split():
        plaintext += str(chr(int(int(num) / key)))
    return plaintext


def saveroomsandcodes(rooms, codes, key):
    encryptrooms = []
    for room in rooms:
        encryptrooms.append(pickle.dumps(room))
    newline(encrypttext(encryptrooms, key))
    newline(encrypttext(codes, key))


def extractroomsandcodes(key):
    codes = decrypttext(getlines()[-1], key)[1:-1].split("', '")
    codes[0] = codes[0][1:]
    codes[-1] = codes[0][:]
    return decrypttext(getlines()[-2]), codes
