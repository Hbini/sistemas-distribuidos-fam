"""
Aula 07: Paradigma PUBLISH/SUBSCRIBE com um broker (intermediário).

    publicador --PUB cardapio "Hoje tem feijoada"--> [ BROKER ] --> todos os assinantes de "cardapio"

Desacoplamento:
  * espacial: publicador e assinante não sabem o endereço um do outro;
  * de sincronização: o publicador não espera os assinantes processarem.

Protocolo de texto (o mesmo para clientes Python e Java), uma linha por comando:
    SUB <topico>                 assina um tópico (a conexão fica aberta recebendo)
    PUB <topico> <mensagem...>   publica uma mensagem no tópico
O broker entrega aos assinantes:  MSG <topico> <mensagem...>

Executar:
    python broker_pubsub.py                       (porta 9300)
    python cliente_pubsub.py sub cardapio         (um ou mais terminais)
    python cliente_pubsub.py pub cardapio "Hoje tem feijoada"
"""

import socket
import threading

PORTA = 9300
assinantes: dict[str, list[socket.socket]] = {}
trava = threading.Lock()


def publicar(topico: str, mensagem: str) -> int:
    linha = f"MSG {topico} {mensagem}\n".encode("utf-8")
    entregues = 0
    with trava:
        for conexao in list(assinantes.get(topico, [])):
            try:
                conexao.sendall(linha)
                entregues += 1
            except OSError:
                assinantes[topico].remove(conexao)      # assinante desconectou
    return entregues


def atender(conexao: socket.socket, endereco) -> None:
    with conexao.makefile("r", encoding="utf-8") as entrada:
        for linha in entrada:
            partes = linha.rstrip("\n").split(" ", 2)
            if partes[0] == "SUB" and len(partes) >= 2:
                with trava:
                    assinantes.setdefault(partes[1], []).append(conexao)
                print(f"[broker] {endereco[0]}:{endereco[1]} assinou '{partes[1]}'")
            elif partes[0] == "PUB" and len(partes) == 3:
                n = publicar(partes[1], partes[2])
                print(f"[broker] '{partes[1]}': {partes[2]!r} entregue a {n} assinante(s)")
                conexao.sendall(f"OK {n}\n".encode())


def main() -> None:
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORTA))
    srv.listen()
    print(f"[broker] pub/sub na porta {PORTA}")
    while True:
        c, e = srv.accept()
        threading.Thread(target=atender, args=(c, e), daemon=True).start()


if __name__ == "__main__":
    main()
