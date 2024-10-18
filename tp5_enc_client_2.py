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
        
def convert_input(msg):
    x, operator, y = verif_input(msg)  # On vérifie et obtient x, operator, y

    # Conversion des entiers en bytes
    x_bytes = x.to_bytes(4, byteorder='big', signed=True)
    y_bytes = y.to_bytes(4, byteorder='big', signed=True)
    
    # Détermination de l'opérateur
    if operator == '+':
        operator_byte = b'\x00'  # 00 pour addition
    elif operator == '-':
        operator_byte = b'\x01'  # 01 pour soustraction
    elif operator == '*':
        operator_byte = b'\x02'  # 02 pour multiplication
    else:
        raise ValueError("Opérateur non reconnu")  # Erreur si l'opérateur est inconnu
    
    # Construction du payload
    payload = x_bytes + operator_byte + y_bytes  # On concatène les bytes
    return payload
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.10.10.11', 13337))

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")

verif_input(msg)

payload = convert_input(msg)
print("calcule envoyer : " + payload)
# On envoie
s.send(payload)


# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
