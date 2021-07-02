from tkinter import *
import random
from random import seed
from random import randint
import numpy as np
from numpy.linalg import det, inv


def findN(p, q):
    return p*q


def factor(n):
    d = 2
    factors = []
    while n >= d*d:
        if n % d == 0:
            n = int(n/d)
            factors.append(d)
        else:
            d = d+1
        if n > 1:
            factors.append(n)
    return factors


def computeGCD(x, y):

    while(y):
        x, y = y, x % y

    return x


def isPrime(n):
    return len(factor(n)) == 1


def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # return gcd, x, y
    return old_r, old_s, old_t


def ModularInv(a, b):
    gcd, x, y = egcd(a, b)
    if x < 0 :
        x += b
    return x

# this is my simple function to find e based on random generation untill gcd( e, phi) == 1


def finde(phi):
    e = 0
    seed(1)
    while computeGCD(e, phi) != 1:
        e = randint(0, phi / 2)
    return e


def encrypt(e, n, msg):
    cipher = ""
    for c in msg:
        m = ord(c)
        cipher += str(pow(m, e, n)) + " "
    return cipher


def findPhin(p, q):
    return (p-1)*(q-1)


class Window(Frame):

    def __init__(self, master=None):

        self.msgToEnc = StringVar()
        self.p = 13
        self.q = 11
        self.n = 0
        self.phiN = 0
        self.e = 0
        self.d = 0
        self.enc = ""
        self.dec = ""
        self.valueBuffer = 0
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("Kaiahs Com. Sec. Project")

        self.pack(fill=BOTH, expand=1)

        text = Label(self, text='Enter text bellow :')
        text.place(x=10, y=20)

        entry = Entry(self, textvariable=self.msgToEnc)
        entry.place(x=10, y=50)

        submitButton = Button(self, text="Submit", padx=10, pady=5, fg="white",
                              bg="#263DDD", command=self.holdUserMsg)
        submitButton.place(x=200, y=50)

        encUserInput = Button(self, text="Encrypt", padx=10, pady=5,
                              fg="white", bg="#263DDD",
                              command=self.encHandeler)
        encUserInput.place(x=280, y=50)

        dcrUserInput = Button(self, text="Decrypt", padx=10, pady=5,
                              fg="white", bg="#263DDD",
                              command=self.decrypt)
        dcrUserInput.place(x=200, y=80)

        bruteUserInput = Button(self, text="Brute Force", padx=10,
                                pady=5, fg="white", bg="#263DDD",
                                command=self.bruteForce)
        bruteUserInput.place(x=280, y=80)

        clearButton = Button(self, text="Clear", command=self.init_window)

        clearButton.place(x=400, y=50)

        quitButton = Button(self, text="Quit", command=self.client_exit)

        quitButton.place(x=400, y=80)

    def client_exit(self):
        exit()

    def holdUserMsg(self):
        text = Label(self, text='Your Text is : ' + self.msgToEnc.get())
        text.place(x=10, y=80)

    def bruteForce(self):
        seed(7)
        self.valueBuffer += 30
        publicKey = self.e
        primes = [3, 5, 7, 11, 13]
        p = random.choice(primes)
        q = random.choice(primes)
        N = p * q
        randPhi = findPhin(p, q)
        rande = finde(randPhi)
        bruteD = ModularInv(publicKey, randPhi)
        while rande != publicKey and (rande <= randPhi):
            p = random.choice(primes)
            q = random.choice(primes)
            N = findN(p, q)
            randPhi = findPhin(p, q)
            rande = finde(randPhi)

        bruteD = ModularInv(publicKey, randPhi)

        msg = ""
        parts = self.enc.split()
        for part in parts:
            if part:
                c = int(part)
                msg += chr(pow(c, bruteD, N))
        text3 = Label(self, text='Your Brute dec text is :' + msg)
        text3.place(x=10, y=(200+self.valueBuffer))

    def encHandeler(self):
        p = 13
        q = 11
        msg = self.msgToEnc.get()
        n = findN(p, q)
        self.n = n
        phiN = findPhin(p, q)
        e = finde(phiN)
        self.e = e
        d = ModularInv(e, phiN)
        self.d = d
        enc = encrypt(e, n, msg)
        text = Label(self, text='Your enc text is :' + enc)
        text.place(x=10, y=120)
        self.enc = enc

    def decrypt(self):
        msg = ""
        parts = self.enc.split()
        for part in parts:
            if part:
                c = int(part)
                msg += chr(pow(c, self.d, self.n))
        text = Label(self, text='Your dec text is :' + msg)
        text.place(x=10, y=160)


root = Tk()

root.geometry("600x400")

app = Window(root)

root.mainloop()
