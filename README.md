# TP5 DEV : Coding Encoding Decoding OPTIMIZE

## 1. Optimisation avec headers

🌞 tp5_enc_client_1.py

```
[yanice@localhost TP5_DEV_Encoding]$ python tp5_enc_client_1.py
Calcul à envoyer: 5+5
b'\x00\x00\x00\x035+5<fin>'
Résultat du serveur : 10
```

🌞 tp5_enc_serveur_1.py

```
[yanice@localhost TP5_DEV_Encoding]$ python tp5_enc_server_1.py
En attente de connexion...
Lecture des 3 prochains octets
Received from client 5+5
```

## 2. Optimisation avec taille fixe et connue

🌞 tp5_enc_client_2.py

🌞 tp5_enc_server_2.py

