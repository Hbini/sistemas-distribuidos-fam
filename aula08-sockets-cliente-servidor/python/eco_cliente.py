"""
Aula 08: cliente do servidor de eco.
Executar: python eco_cliente.py [ip_do_servidor]
Funciona com o servidor Python e com o EcoServidor.java (mesma porta 9500).
"""
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORTA = 9500

# create_connection = socket() + connect() em uma linha
with socket.create_connection((HOST, PORTA)) as cliente:
    print(f"Conectado a {HOST}:{PORTA}. Digite mensagens (linha vazia para sair).")
    while True:
        msg = input("> ")
        if not msg:
            break
        cliente.sendall(msg.encode("utf-8"))
        print(cliente.recv(1024).decode("utf-8"))
