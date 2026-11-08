"""
Aula 13: Tolerância a falhas: DETECÇÃO por HEARTBEAT e TIMEOUT.

Cada nó manda "estou vivo" (heartbeat) por UDP a cada 1 segundo.
O monitor marca como SUSPEITO quem ficar 3 s sem sinal e como FALHO após 6 s.

Executar:
    python detector_falhas_heartbeat.py monitor
    python detector_falhas_heartbeat.py no servidor-A
    python detector_falhas_heartbeat.py no servidor-B
    java ../java/NoHeartbeat.java servidor-Java          (compatível)
Feche um nó com Ctrl+C e observe o monitor.
"""

import socket
import sys
import threading
import time

PORTA = 9900
SUSPEITA, FALHA = 3.0, 6.0


def monitor() -> None:
    ultimo: dict[str, float] = {}
    trava = threading.Lock()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORTA))

    def receber() -> None:
        while True:
            dados, _ = sock.recvfrom(256)
            nome = dados.decode().removeprefix("VIVO ").strip()
            with trava:
                if nome not in ultimo:
                    print(f"[monitor] novo nó: {nome}")
                ultimo[nome] = time.time()

    threading.Thread(target=receber, daemon=True).start()
    print(f"[monitor] ouvindo heartbeats na porta UDP {PORTA}")
    while True:
        time.sleep(2)
        agora = time.time()
        with trava:
            situacao = []
            for nome, t in sorted(ultimo.items()):
                atraso = agora - t
                estado = "OK" if atraso < SUSPEITA else ("SUSPEITO" if atraso < FALHA else "FALHO")
                situacao.append(f"{nome}={estado}({atraso:.0f}s)")
        print("[monitor] " + "  ".join(situacao))


def no(nome: str) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[{nome}] enviando heartbeat a cada 1 s (Ctrl+C simula a falha)")
    while True:
        sock.sendto(f"VIVO {nome}".encode(), ("127.0.0.1", PORTA))
        time.sleep(1)


if __name__ == "__main__":
    monitor() if sys.argv[1] == "monitor" else no(sys.argv[2])
