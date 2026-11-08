"""
Aula 08: servidor CONCORRENTE: uma thread para cada cliente.

Teste o problema do servidor iterativo: abra dois eco_cliente.py contra o
eco_servidor.py. O segundo fica "pendurado" até o primeiro sair. Com este
servidor, os dois são atendidos ao mesmo tempo.

Executar: python servidor_multicliente.py   (mesma porta 9500 do eco)
"""
import socket
import threading

clientes_ativos = 0
trava = threading.Lock()


def atender(conexao: socket.socket, endereco) -> None:
    global clientes_ativos
    with trava:
        clientes_ativos += 1
    nome = threading.current_thread().name
    print(f"[{nome}] atendendo {endereco} | clientes ativos: {clientes_ativos}")
    with conexao:
        while dados := conexao.recv(1024):
            conexao.sendall(f"ECO ({nome}): {dados.decode().upper()}".encode())
    with trava:
        clientes_ativos -= 1
    print(f"[{nome}] {endereco} saiu | clientes ativos: {clientes_ativos}")


servidor = socket.socket()
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", 9500))
servidor.listen()
print("Servidor multicliente na porta 9500")
while True:
    c, e = servidor.accept()
    threading.Thread(target=atender, args=(c, e), daemon=True).start()
