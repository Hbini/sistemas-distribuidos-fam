"""
Aula 04: Desempenho e Escalabilidade.
Três modelos de servidor para o MESMO serviço, para medir a diferença:

  sequencial : atende um cliente por vez (os outros esperam na fila)
  thread     : cria uma thread nova para cada cliente (sem limite)
  pool       : usa um número FIXO de threads (pool), reaproveitadas

Cada pedido simula 200 ms de trabalho de E/S (por exemplo, consulta a banco de
dados). É o caso típico de servidores web, em que o gargalo é esperar, não calcular.

Como executar:
    python servidor_modelos.py sequencial 8000
    python servidor_modelos.py thread 8000
    python servidor_modelos.py pool 8000 4        (pool com 4 threads)
Em outro terminal, gere carga com gerador_carga.py.
"""

import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

TEMPO_SERVICO = 0.2   # segundos de "trabalho" por pedido


def atender(conexao: socket.socket) -> None:
    with conexao:
        pedido = conexao.recv(1024)
        if not pedido:
            return
        time.sleep(TEMPO_SERVICO)                         # simula E/S (banco, disco, outra API)
        conexao.sendall(b"OK " + pedido.strip() + b"\n")


def main() -> None:
    modo = sys.argv[1] if len(sys.argv) > 1 else "sequencial"
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    tamanho_pool = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", porta))
    servidor.listen(1024)       # fila de conexões pendentes (backlog)
    print(f"Servidor no modo '{modo}' na porta {porta}"
          + (f" com {tamanho_pool} threads" if modo == "pool" else ""))
    print(f"Capacidade teórica: sequencial = {1 / TEMPO_SERVICO:.0f} pedidos/s; "
          f"pool = {tamanho_pool / TEMPO_SERVICO:.0f} pedidos/s")

    pool = ThreadPoolExecutor(max_workers=tamanho_pool) if modo == "pool" else None
    while True:
        conexao, _ = servidor.accept()
        if modo == "sequencial":
            atender(conexao)                                   # bloqueia até terminar
        elif modo == "thread":
            threading.Thread(target=atender, args=(conexao,), daemon=True).start()
        else:
            pool.submit(atender, conexao)                      # entra na fila do pool


if __name__ == "__main__":
    main()
