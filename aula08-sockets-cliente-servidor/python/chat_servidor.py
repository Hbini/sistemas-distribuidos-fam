"""
Aula 08: servidor de CHAT em grupo sobre TCP.

Protocolo (texto, uma linha por mensagem; igual ao ChatServidor.java):
    1ª linha enviada pelo cliente: o apelido
    linhas seguintes: mensagens, que o servidor repassa a TODOS os outros
    comando especial: /quem  -> lista quem está online

Executar: python chat_servidor.py      e vários   python chat_cliente.py <apelido>
"""
import socket
import threading

PORTA = 9600
clientes: dict[socket.socket, str] = {}
trava = threading.Lock()


def difundir(texto: str, exceto: socket.socket | None = None) -> None:
    with trava:
        for c in list(clientes):
            if c is not exceto:
                try:
                    c.sendall((texto + "\n").encode("utf-8"))
                except OSError:
                    clientes.pop(c, None)


def atender(conexao: socket.socket) -> None:
    entrada = conexao.makefile("r", encoding="utf-8")
    apelido = entrada.readline().strip() or "anônimo"
    with trava:
        clientes[conexao] = apelido
    difundir(f"*** {apelido} entrou no chat ***")
    try:
        for linha in entrada:
            linha = linha.rstrip("\n")
            if linha == "/quem":
                with trava:
                    nomes = ", ".join(clientes.values())
                conexao.sendall(f"*** online: {nomes}\n".encode("utf-8"))
            elif linha:
                difundir(f"[{apelido}] {linha}", exceto=conexao)
    finally:
        with trava:
            clientes.pop(conexao, None)
        difundir(f"*** {apelido} saiu ***")
        conexao.close()


srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", PORTA))
srv.listen()
print(f"Chat na porta {PORTA}")
while True:
    c, _ = srv.accept()
    threading.Thread(target=atender, args=(c,), daemon=True).start()
