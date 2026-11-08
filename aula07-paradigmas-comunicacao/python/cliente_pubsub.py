"""
Aula 07: cliente do broker pub/sub (publicador ou assinante).
    python cliente_pubsub.py sub cardapio
    python cliente_pubsub.py pub cardapio "Hoje tem feijoada"
"""
import socket
import sys

HOST, PORTA = "127.0.0.1", 9300
modo, topico = sys.argv[1], sys.argv[2]

with socket.create_connection((HOST, PORTA)) as s:
    if modo == "sub":
        s.sendall(f"SUB {topico}\n".encode())
        print(f"Assinando '{topico}'. Aguardando mensagens (Ctrl+C para sair)...")
        for linha in s.makefile("r", encoding="utf-8"):
            _, top, msg = linha.rstrip("\n").split(" ", 2)
            print(f"[{top}] {msg}")
    else:
        s.sendall(f"PUB {topico} {' '.join(sys.argv[3:])}\n".encode("utf-8"))
        print("Broker respondeu:", s.makefile("r").readline().strip())
