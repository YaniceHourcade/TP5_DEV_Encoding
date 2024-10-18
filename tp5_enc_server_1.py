import socket
import struct
import re

def recv_all(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.10.10.11', 13337))  

s.listen(1)
print("En attente de connexion...")
conn, addr = s.accept()

while True:
    try:
        # On reçoit la string Hello du client
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())
        
        # Lecture de l'en-tête (taille du message)
        header = recv_all(conn, 4)
        if not header:
            break
        
        message_length = struct.unpack('!I', header)[0]
        
        # Lecture du message selon la taille définie dans l'en-tête
        data = recv_all(conn, message_length)
        if not data:
            print("Déconnexion du client.")
            break
        
        # Vérification si le message se termine par une séquence de fin spécifique
        if not data.endswith(b'<clafin>'):
            print("Séquence de fin manquante.")
            break
        
        calc_expression = data[:-len('<clafin>')].decode().strip()
        print(f"Calcul reçu : {calc_expression}")

        # Evaluation et envoi du résultat
        res = eval(calc_expression)
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()


