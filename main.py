from interface import Person, Eve, Bob, full_clear
from time import sleep
import os

def clear():
    os.system('clear')
clear()

full_clear()
print('Bob a Alice si chtějí vyměnit zprávu')
print('Jejich komunikaci se snaží odposlouchávat Eva')
print('Aby Eva nezjistila, co si povídají, rozhodli se použít aplikaci s RSA šifrováním')

sleep(4)
print('Přihlašuje se Alice')
alice = Person('alice')
sleep(2)
print('Alice si generuje soukromý a veřejný klíč')

sleep(4)
print('Přihlašuje se Bob')
bob = Bob('bob')
sleep(2)
print('Bob si generuje soukromý a veřejný klíč')

sleep(4)
print('Bob posílá Alici zprávu: (zadej číslo)')
message = int(input())
print('Aby ji Eva nezjistila, Bob použije k šifrování veřejný klíč Alice')
bob.send(message, 'alice')
sleep(2)
print('Eva jejich zprávu zachytí, ale kvůli šifrování ji nedokáže přečíst')
print('Eva přijala zprávu ', end='')
f = open("encrypted_messages.txt", 'r')
for line in f:
    message = line.split(sep=',')
    if 'alice' == message[0]:
        print(message[1])
        break
f.close()

sleep(4)
print('Alice si přijatou zprávu rozšifruje pomocí soukromého klíče:')
alice.read()
print('.')
input()
print('Alice posílá Bobovi zprávu: (zadej číslo)')
message = int(input())
print('Aby ji Eva nezjistila, použije k šifrování veřejný klíč Boba')
alice.send(message, 'bob')

sleep(2)
print('Bob používá starou verzi aplikace, která má bezpečnostní slabinu')
sleep(2)
print('Eva tuto slabinu zná a dokáže ji využít, tudíž zjistí Bobův klíč')
eva = Eve('eva')
eva.crack_encryption('bob')

print('Eva přijala zprávu ', sep='')
f = open("encrypted_messages.txt", 'r')
for line in f:
    message = line.split(sep=',')
    if 'bob' == message[0]:
        print(message[1])
        break

f.close()
print('.')
input()
print('Eva zná Bobův soukromý klíč, a tudíž je schopná rozluštit zprávu pro Boba:')
eva.open_cracked_message('bob')
sleep(4)
print('Bob si přijatou zprávu rozšifruje pomocí soukromého klíče:')
bob.read()
