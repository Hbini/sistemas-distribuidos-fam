"""
Aula 08: Sockets TCP: o servidor de ECO mais simples possível, passo a passo.

O ciclo de vida de um SERVIDOR TCP:
    socket()  ->  bind()  ->  listen()  ->  accept()  ->  recv()/send()  ->  close()
O ciclo de vida de um CLIENTE TCP:
    socket()  ->  connect()  ->  send()/recv()  ->  close()

Este servidor atende UM cliente por vez (iterativo). O multicliente está em
servidor_multicliente.py.

Executar: python eco_servidor.py        e depois   python eco_cliente.py
"""

import socket

HOST = "0.0.0.0"   # 0.0.0.0 = aceita conexões de qualquer interface de rede
PORTA = 9500       # portas abaixo de 1024 exigem privilégio de administrador

# 1. socket(): cria o "telefone". AF_INET = IPv4, SOCK_STREAM = TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite reaproveitar a porta logo após fechar o programa (evita "Address already in use")
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 2. bind(): associa o socket a um endereço IP e a uma porta ("número do telefone")
servidor.bind((HOST, PORTA))

# 3. listen(): passa a aceitar ligações; 5 = tamanho da fila de espera
servidor.listen(5)
print(f"Servidor de eco ouvindo em {HOST}:{PORTA}")

while True:
    # 4. accept(): BLOQUEIA até um cliente conectar. Devolve um NOVO socket,
    #    exclusivo para conversar com esse cliente, e o endereço dele.
    conexao, (ip, porta_cliente) = servidor.accept()
    print(f"Cliente conectado: {ip}:{porta_cliente}")
    with conexao:
        while True:
            # 5. recv(): lê até 1024 bytes. b"" (vazio) significa que o cliente fechou.
            dados = conexao.recv(1024)
            if not dados:
                break
            texto = dados.decode("utf-8")
            print(f"  recebido: {texto!r}")
            # 6. sendall(): devolve os dados (garante o envio de todos os bytes)
            conexao.sendall(f"ECO: {texto.upper()}".encode("utf-8"))
    # 7. close(): o "with" fecha a conexão automaticamente
    print(f"Cliente {ip}:{porta_cliente} desconectou")
