"""
Aula 07: Paradigma FILA DE MENSAGENS (ponto a ponto, "competing consumers").

Diferença para o pub/sub:
  * pub/sub: CADA assinante recebe uma cópia da mensagem;
  * fila   : cada mensagem é entregue a APENAS UM consumidor
             (bom para dividir tarefas: pedidos da cozinha, e-mails a enviar...).

As mensagens ficam guardadas no broker até alguém consumir (persistência em memória).

Protocolo:  PUT <fila> <msg>  -> OK      |      GET <fila>  -> MSG <msg>  ou  VAZIA

Executar:
    python fila_mensagens.py broker
    python fila_mensagens.py consumidor cozinha Chef-A      (abra 2 ou 3 consumidores)
    python fila_mensagens.py produtor cozinha 10            (gera 10 pedidos)
"""

import collections
import socket
import sys
import threading
import time

PORTA = 9400
filas: dict[str, collections.deque] = collections.defaultdict(collections.deque)
trava = threading.Lock()


def atender(conexao) -> None:
    with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
        for linha in entrada:
            partes = linha.rstrip("\n").split(" ", 2)
            with trava:
                if partes[0] == "PUT":
                    filas[partes[1]].append(partes[2])
                    resposta = f"OK {len(filas[partes[1]])}"
                elif partes[0] == "GET":
                    fila = filas[partes[1]]
                    resposta = f"MSG {fila.popleft()}" if fila else "VAZIA"
                else:
                    resposta = "ERRO"
            conexao.sendall((resposta + "\n").encode("utf-8"))


def broker() -> None:
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORTA))
    srv.listen()
    print(f"[fila] broker na porta {PORTA}")
    while True:
        c, _ = srv.accept()
        threading.Thread(target=atender, args=(c,), daemon=True).start()


def produtor(fila: str, quantidade: int) -> None:
    with socket.create_connection(("127.0.0.1", PORTA)) as s, s.makefile("r") as r:
        for i in range(1, quantidade + 1):
            s.sendall(f"PUT {fila} pedido-{i}\n".encode())
            print(f"enviei pedido-{i} -> {r.readline().strip()}")


def consumidor(fila: str, nome: str) -> None:
    with socket.create_connection(("127.0.0.1", PORTA)) as s, s.makefile("r") as r:
        while True:
            s.sendall(f"GET {fila}\n".encode())
            resposta = r.readline().strip()
            if resposta == "VAZIA":
                time.sleep(0.5)                      # nada na fila: espera um pouco (polling)
                continue
            print(f"[{nome}] preparando {resposta[4:]}...")
            time.sleep(1)                            # tempo de "preparo"


if __name__ == "__main__":
    modo = sys.argv[1]
    if modo == "broker":
        broker()
    elif modo == "produtor":
        produtor(sys.argv[2], int(sys.argv[3]))
    else:
        consumidor(sys.argv[2], sys.argv[3])
