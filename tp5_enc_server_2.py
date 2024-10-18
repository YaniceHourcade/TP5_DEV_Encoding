import socket
import struct

def convert_data(data):
    # Extraction des nombres et de l'opérateur du message
    x_bytes = data[:4]
    operator_byte = data[4:5]
    y_bytes = data[5:9]
    
    # Conversion des bytes en entiers
    x = struct.unpack('>i', x_bytes)[0]  # '>i' pour big-endian
    y = struct.unpack('>i', y_bytes)[0]  # '>i' pour big-endian
    
    # Détermination de l'opérateur
    if operator_byte == b'\x00':
        operator = '+'
    elif operator_byte == b'\x01':
        operator = '-'
    elif operator_byte == b'\x02':
        operator = '*'
    else:
        raise ValueError("Opérateur non reconnu")
    
    # Construction de l'expression arithmétique
    expression = f"{x} {operator} {y}"
    return expression
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.10.10.11', 13337))  

s.listen(1)
print("En attente de connexion...")
conn, addr = s.accept()

while True:

    try:
        # On reçoit le calcul du client
        data = conn.recv(1024)

        if not data:
            print("Connexion fermée par le client.")
            break
        
        expression = convert_data(data)
        print("calcul du client: " + expression)
        
        # Evaluation et envoi du résultat
        res  = eval(data.decode())
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
