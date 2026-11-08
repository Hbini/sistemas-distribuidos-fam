"""
Aula 09: Paradigma SERVIÇO DE GRUPO com IP MULTICAST.

Uma única mensagem enviada para o endereço do GRUPO (224.1.1.1) é entregue
pela rede a TODOS os membros que entraram no grupo. O remetente não precisa
saber quem são nem quantos são os membros.

    unicast  : 1 -> 1      (TCP, UDP comum)
    multicast: 1 -> grupo  (este exemplo)
    broadcast: 1 -> todos da rede local

Executar (vários terminais, ou várias máquinas da MESMA rede local):
    python multicast_grupo.py Ana
    python multicast_grupo.py Bruno
    java   ../java/MulticastMembro.java Carla       (membro Java no mesmo grupo)

Observação: alguns roteadores Wi-Fi e redes corporativas bloqueiam multicast.
No laboratório com cabo costuma funcionar. Em uma única máquina sempre funciona.
"""

import socket
import struct
import sys
import threading

GRUPO = "224.1.1.1"   # faixa 224.0.0.0 a 239.255.255.255 é reservada para multicast
PORTA = 5007
nome = sys.argv[1] if len(sys.argv) > 1 else "membro"


def receber() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # vários membros na mesma máquina
    sock.bind(("", PORTA))
    # ENTRAR NO GRUPO (IGMP join): avisa a placa de rede para aceitar pacotes de 224.1.1.1
    pedido = struct.pack("4sl", socket.inet_aton(GRUPO), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, pedido)
    while True:
        dados, origem = sock.recvfrom(1024)
        print(f"\r{dados.decode('utf-8')}   (de {origem[0]})\n> ", end="")


threading.Thread(target=receber, daemon=True).start()

envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
envio.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)  # TTL 1 = não sai da rede local
print(f"{nome} entrou no grupo {GRUPO}:{PORTA}. Digite mensagens:")
envio.sendto(f"*** {nome} entrou no grupo".encode(), (GRUPO, PORTA))
for linha in sys.stdin:
    envio.sendto(f"[{nome}] {linha.strip()}".encode("utf-8"), (GRUPO, PORTA))
