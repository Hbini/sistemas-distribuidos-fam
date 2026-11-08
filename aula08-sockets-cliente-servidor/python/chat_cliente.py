"""
Aula 08: cliente de chat. Usa DUAS threads:
  * a principal lê o teclado e envia;
  * uma secundária fica recebendo mensagens do servidor a qualquer momento.
Executar: python chat_cliente.py <apelido> [ip_do_servidor]
"""
import socket
import sys
import threading

apelido = sys.argv[1] if len(sys.argv) > 1 else "aluno"
host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
sock = socket.create_connection((host, 9600))
sock.sendall((apelido + "\n").encode("utf-8"))


def receber() -> None:
    for linha in sock.makefile("r", encoding="utf-8"):
        print(linha, end="")
    print("Conexão encerrada pelo servidor.")


threading.Thread(target=receber, daemon=True).start()
print("Digite mensagens (/quem lista os usuários, /sair encerra).")
for linha in sys.stdin:
    if linha.strip() == "/sair":
        break
    sock.sendall(linha.encode("utf-8"))
sock.close()
