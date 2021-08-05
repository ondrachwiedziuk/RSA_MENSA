from random import randint, sample
from sympy import gcd, sieve, isprime


def crack(n):
    """Function that find p, q for given product n.

    Args: n(int) -> product of two primes
    Return: list(int) -> primes for given n
    """
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
    """Balanced primes generator

    Return: list(int) -> primes
    """
    primes = list(sieve.primerange(1000, 2000))
    balanced_primes = list()
    for i in range(1, len(primes) - 1):
        if primes[i - 1] + primes[i + 1] == primes[i] * 2:
            balanced_primes.append(primes[i])
    return sample(balanced_primes, k=2)


def prime_gen():
    """Primes generator

    Return: list(int) -> primes
    """
    primes = list(sieve.primerange(1000, 2000))
    return sample(primes, k=2)


def euler_function(primes):
    """Euler function for two primes

    Args: list(int) -> primes
    Return: (int) -> Euler function of p, q
    """
    p = primes[0]
    q = primes[1]
    return (p - 1) * (q - 1)


def decryption(c, d, n):
    """Function for decrypt RSA cipher by private key

    Args: c (int) -> encrypted message
          d (int) -> private key
          n (int) -> product of two primes
    Return: (int) -> message
    """
    return c**d % n


def encryption(message, e, n):
    """Function for encrypt RSA cipher by public key

    Args: c (int) -> message
          d (int) -> public key
          n (int) -> product of two primes
    Return: (int) -> encrypted message
    """
    return message**e % n

def clear(name):
    """Clear content of text files by name

    Args: name (str) -> text file name
    """
    f = open(name, 'r+')
    f.truncate(0)
    f.close()


def full_clear():
    """Clear all text files
    """
    files = ["public_key.txt", "encrypted_messages.txt"]
    for name in files:
        clear(name)


class Person:
    def __init__(self, name):
        self.name = name
        self.private_key = None
        self.create_key()

    def create_key(self):
        """Set pair of keys for a person
        """
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

    def send(self, message, receiver):
        """Send encrypted message to chosen person by writing it to corresponding text file

        Args: mesage (int) -> message
              receiver (str) -> A person who will get a message
        """
        public = open("public_key.txt", 'r')
        for line in public:
            x = line.split(sep=',')
            if x[0] == receiver:
                public_key = x
        n = int(public_key[1])
        e = int(public_key[2])
        encrypted = encryption(message, e, n)
        f = open("encrypted_messages.txt", 'a')
        f.write(receiver + ',' + str(encrypted) + '\n')
        f.close()

    def read(self):
        """Read last message written in corresponding text file and print it in terminal
        """
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
        """Set pair of keys for a person with weak generator
        """
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
        """Crack a private key of given person, require weak key generator

        Args: cracked_person (str) -> Person given to be cracked
        """
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
        """Find a cracked private key for given person

        Args: name (str) -> Name of given person
        Return (Crack) default None -> Crack object containing name and private key of given person
        """
        return next((crack for crack in self.cracks if crack.name == name), None)

    def open_cracked_message(self, cracked_person):
        """Read last message of cracked person printing it to terminal

        Args: cracked_person (str) -> name of cracked person.
        """
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
