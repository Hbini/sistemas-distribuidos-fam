"""Aula 06: cliente Python do servidor binário (desfaz o marshalling)."""
import socket
import struct

FORMATO = "!I20sHd"
with socket.create_connection(("127.0.0.1", 9100)) as s:
    dados = b""
    while len(dados) < struct.calcsize(FORMATO):
        dados += s.recv(1024)
pid, prod, qtd, preco = struct.unpack(FORMATO, dados)
print(f"id={pid} produto={prod.rstrip(bytes(1)).decode()} quantidade={qtd} preço={preco}")
