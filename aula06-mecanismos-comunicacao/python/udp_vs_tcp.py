"""
Aula 06: UDP x TCP.

UDP: sem conexão, sem garantia de entrega nem de ordem. Rápido e leve.
TCP: orientado a conexão, entrega confiável e ordenada (retransmite o que se perde).

Para ver PERDA em uma única máquina (onde a rede local quase nunca perde nada),
o servidor UDP DESCARTA de propósito 30% dos datagramas, simulando uma rede ruim.
O cliente envia 50 mensagens e conta quantas respostas chegaram.

Executar (2 terminais):
    python udp_vs_tcp.py servidor
    python udp_vs_tcp.py cliente
"""

import random
import socket
import sys

PORTA = 9200
TAXA_PERDA = 0.30


def servidor() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # DGRAM = UDP
    sock.bind(("0.0.0.0", PORTA))
    print(f"[udp] servidor na porta {PORTA}, descartando {TAXA_PERDA:.0%} dos pacotes")
    while True:
        dados, origem = sock.recvfrom(1024)          # cada recvfrom = um datagrama inteiro
        if random.random() < TAXA_PERDA:
            print(f"[udp] (perdido) {dados.decode()}")
            continue
        sock.sendto(b"eco: " + dados, origem)        # responde para quem mandou


def cliente() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.3)                              # UDP não avisa perda: usamos timeout
    recebidas = 0
    for i in range(50):
        sock.sendto(f"mensagem {i}".encode(), ("127.0.0.1", PORTA))
        try:
            sock.recvfrom(1024)
            recebidas += 1
        except socket.timeout:
            print(f"mensagem {i}: sem resposta (perdida)")
    print(f"\nRespostas recebidas: {recebidas}/50")
    print("Com TCP, a própria pilha de rede retransmitiria e todas chegariam (mais lentamente).")
    print("Para ter confiabilidade sobre UDP, a APLICAÇÃO precisa implementar retransmissão (exercício 2).")


if __name__ == "__main__":
    servidor() if sys.argv[1:] == ["servidor"] else cliente()
