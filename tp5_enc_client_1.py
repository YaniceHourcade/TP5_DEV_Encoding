import socket
import re

def verif_input(msg):
    pattern = r"^\s*(-?\d+)\s*([\+\-\*])\s*(-?\d+)\s*$"
    match = re.match(pattern, msg)
    
    if not match:
        print("Format incorrect. Utilisez le format: nombre opérateur nombre (ex: 3 + 3)")
        exit()
    
    x, operator, y = match.groups()
    
    if not (-1048575 <= int(x) <= 1048575 and -1048575 <= int(y) <= 1048575):
        print("Les nombres doivent être compris entre -1048575 et 1048575")
        exit()
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.10.10.11', 13337))

s.send('Hello'.encode())

# On reçoit la string Hello
data = s.recv(1024)
print(f"Serveur dit : {data.decode()}")

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")

verif_input(msg)

encoded_msg = msg.encode('utf-8')

header = len(encoded_msg).to_bytes(4, byteorder='big')

fin = '<fin>'.encode('utf-8')

payload = header + encoded_msg + fin

print(payload)
# On envoie
s.send(payload)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(f"Résultat du serveur : {s_data.decode()}")
s.close()
