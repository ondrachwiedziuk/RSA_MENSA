from random import randint, sample
from sympy import gcd, sieve, isprime


def crack(n):
    primes = list(sieve.primerange(1000, 2000))
    balanced_primes = list()
    for i in range(1, len(primes) - 1):
        if primes[i - 1] + primes[i + 1] == primes[i] * 2:
            balanced_primes.append(primes[i])
    for i in balanced_primes:
        for j in balanced_primes:
            if i * j == n:
                return [i, j]


def weak_prime_gen():
    primes = list(sieve.primerange(1000, 2000))
    balanced_primes = list()
    for i in range(1, len(primes) - 1):
        if primes[i - 1] + primes[i + 1] == primes[i] * 2:
            balanced_primes.append(primes[i])
    return sample(balanced_primes, k=2)


def prime_gen():
    primes = list(sieve.primerange(1000, 2000))
    return sample(primes, k=2)


def euler_function(primes):
    p = primes[0]
    q = primes[1]
    return (p - 1) * (q - 1)


def decryption(c, d, n):
    return c**d % n


def encryption(message, e, n):
    return message**e % n


def clear(name):
    f = open(name, 'r+')
    f.truncate(0)
    f.close()


def full_clear():
    files = ["public_key.txt", "encrypted_messages.txt"]
    for name in files:
        clear(name)


def clear_test():
    name = "encrypted_message.txt"
    clear(name)


class Person:
    def __init__(self, name):
        self.name = name
        self.private_key = None
        self.create_key()

    def create_key(self):
        primes = prime_gen()
        n = primes[0] * primes[1]
        fi = euler_function(primes)
        while True:
            e = randint(2, fi - 1)
            if gcd(e, fi) == 1:
                break

        d = pow(e, -1, fi)
        public_key = (n, e)
        private_key = (n, d)
        public = open("public_key.txt", 'a')
        public.write(self.name + ',' + str(public_key[0]) + ',' + str(public_key[1]) + '\n')
        public.close()
        self.private_key = private_key

    def send(self, message, reciever):
        public = open("public_key.txt", 'r')
        for line in public:
            x = line.split(sep=',')
            if x[0] == reciever:
                public_key = x
        n = int(public_key[1])
        e = int(public_key[2])
        encrypted = encryption(message, e, n)
        f = open("encrypted_messages.txt", 'a')
        f.write(reciever + ',' + str(encrypted) + '\n')
        f.close()

    def read(self):
        f = open("encrypted_messages.txt", 'r')
        for line in f:
            message = line.split(sep=',')
            if self.name == message[0]:
                encrypted = int(message[1])
        n = self.private_key[0]
        d = self.private_key[1]
        decrypted_message = decryption(encrypted, d, n)
        print(decrypted_message)


class Bob(Person):
    def create_key(self):
        primes = weak_prime_gen()
        n = primes[0] * primes[1]
        fi = euler_function(primes)
        while True:
            e = randint(2, fi - 1)
            if gcd(e, fi) == 1:
                break

        d = pow(e, -1, fi)
        public_key = (n, e)
        private_key = (n, d)
        public = open("public_key.txt", 'a')
        public.write(self.name + ',' + str(public_key[0]) + ',' + str(public_key[1]) + '\n')
        public.close()
        self.private_key = private_key

class Eve(Person):
    cracks = list()

    def crack_encryption(self, cracked_person):
        public = open("public_key.txt", 'r')
        for line in public:
            x = line.split(sep=',')
            if x[0] == cracked_person:
                public_key = x
        n = int(public_key[1])
        e = int(public_key[2])
        cracked_primes = crack(n)
        fi = euler_function(cracked_primes)
        d = pow(e, -1, fi)
        private_key = (n, d)
        self.cracks.append(Crack(cracked_person, private_key))

    def get_cracked(self, name):
        return next((crack for crack in self.cracks if crack.name == name), None)

    def open_cracked_message(self, cracked_person):
        crack = self.get_cracked(cracked_person)
        f = open("encrypted_messages.txt", 'r')
        for line in f:
            message = line.split(sep=',')
            if crack.name == message[0]:
                encrypted = int(message[1])
        n = crack.private_key[0]
        d = crack.private_key[1]
        decrypted_message = decryption(encrypted, d, n)
        print(decrypted_message)


class Crack:
    def __init__(self, name, private_key):
        self.name = name
        self.private_key = private_key


if __name__ == '__main__':
    full_clear()
