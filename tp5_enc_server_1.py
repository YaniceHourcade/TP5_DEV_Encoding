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
        
        chunks = []

        bytes_received = 0
        while bytes_received < msg_len:
            chunk = conn.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')

        chunks.append(chunk)

        bytes_received += len(chunk)

        message_received = b"".join(chunks).decode('utf-8')
        end_check = message_received[-(len(END_MESSAGE)):]
        message = message_received[:len(message_received)-len(END_MESSAGE)]

        if end_check == END_MESSAGE:
            print(f"Received from client {message}")
        else:
            print("Aucun séquence de fin trouvée")
    
        # Evaluation et envoi du résultat
        res = eval(message_received)
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()


