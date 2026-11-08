"""
Aula 06: servidor que envia um pedido em formato BINÁRIO (struct, big-endian).
O cliente pode ser Python ou Java: basta os dois combinarem o MESMO layout.

Layout (34 bytes no total, ordem de rede):
    4 bytes id (inteiro) | 20 bytes produto (UTF-8, completado com zeros) |
    2 bytes quantidade (inteiro curto) | 8 bytes preço (double)

Executar: python servidor_binario.py
Cliente : java ../java/ClienteBinario.java   ou   python cliente_binario.py
"""
import socket
import struct

FORMATO = "!I20sHd"   # 4 + 20 + 2 + 8 = 34 bytes

srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 9100))
srv.listen()
print(f"[servidor-binario] porta 9100, cada mensagem tem {struct.calcsize(FORMATO)} bytes")
while True:
    c, end = srv.accept()
    with c:
        msg = struct.pack(FORMATO, 42, "Pão de queijo".encode("utf-8"), 3, 4.5)
        c.sendall(msg)
        print(f"[servidor-binario] enviei {msg.hex(' ')} para {end[0]}")
