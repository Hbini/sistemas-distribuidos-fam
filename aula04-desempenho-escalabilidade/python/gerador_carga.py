"""
Aula 04: Gerador de carga: simula vários clientes simultâneos e mede
VAZÃO (throughput, pedidos por segundo) e LATÊNCIA (tempo de resposta).

Como executar:
    python gerador_carga.py 127.0.0.1 8000 20 5
        20 = clientes simultâneos, 5 = pedidos de cada cliente (total 100)
"""

import socket
import statistics
import sys
import threading
import time


def cliente(host: str, porta: int, n_pedidos: int, latencias: list[float], trava: threading.Lock) -> None:
    for i in range(n_pedidos):
        t0 = time.perf_counter()
        with socket.create_connection((host, porta), timeout=60) as s:
            s.sendall(f"pedido-{i}\n".encode())
            s.recv(1024)
        with trava:
            latencias.append(time.perf_counter() - t0)


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    n_clientes = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    n_pedidos = int(sys.argv[4]) if len(sys.argv) > 4 else 5

    latencias: list[float] = []
    trava = threading.Lock()
    t0 = time.perf_counter()
    threads = [threading.Thread(target=cliente, args=(host, porta, n_pedidos, latencias, trava))
               for _ in range(n_clientes)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    duracao = time.perf_counter() - t0

    latencias.sort()
    p95 = latencias[int(len(latencias) * 0.95) - 1]
    print(f"Clientes simultâneos : {n_clientes}")
    print(f"Pedidos atendidos    : {len(latencias)} em {duracao:.2f} s")
    print(f"Vazão (throughput)   : {len(latencias) / duracao:.1f} pedidos/s")
    print(f"Latência média       : {statistics.mean(latencias) * 1000:.0f} ms")
    print(f"Latência p95         : {p95 * 1000:.0f} ms  (95% dos pedidos foram mais rápidos que isso)")


if __name__ == "__main__":
    main()
