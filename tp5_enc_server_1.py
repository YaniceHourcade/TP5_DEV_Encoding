import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.10.10.11', 13337))  

s.listen(1)
print("En attente de connexion...")
conn, addr = s.accept()

END_MESSAGE = "<fin>"

while True:
    try:
        header = conn.recv(4)
        if not header:
            break
        
        msg_len = int.from_bytes(header[0:4], byteorder='big')

        print(f"Lecture des {msg_len} prochains octets")
        
        message = conn.recv(msg_len).decode('utf-8')
        
        end_check = conn.recv(len(END_MESSAGE)).decode('utf-8')

        if end_check == END_MESSAGE:
            print(f"Received from client {message}")
        else:
            print("Aucun séquence de fin trouvée")
    
        # Evaluation et envoi du résultat
        res = eval(message)
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()


