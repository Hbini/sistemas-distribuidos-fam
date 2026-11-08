"""
Aula 03: RÉPLICA de um serviço de calculadora.

Várias cópias (réplicas) idênticas deste servidor podem rodar ao mesmo tempo,
em portas ou máquinas diferentes. Se uma cair, as outras continuam atendendo:
isso aumenta a CONFIABILIDADE (disponibilidade) do sistema.

Ao iniciar, a réplica se registra no serviço de nomes com o nome "calculadora".

Protocolo (texto): "SOMA 2 3", "MULT 4 5", "SUB 9 1", "DIV 8 2"
Resposta:          "5.0 (atendido por replica-7001@nome-da-maquina)"

Como executar (um terminal para cada réplica):
    python servidor_replica.py 7001
    python servidor_replica.py 7002
    python servidor_replica.py 7003 --host-nomes 192.168.0.10   (serviço de nomes em outra máquina)

Para simular uma FALHA: feche uma das réplicas com Ctrl+C.
"""

import argparse
import socket
import threading

# FLEXIBILIDADE: para acrescentar uma operação nova basta incluir uma linha
# neste dicionário. Nenhuma outra parte do código precisa mudar.
OPERACOES = {
    "SOMA": lambda a, b: a + b,
    "SUB": lambda a, b: a - b,
    "MULT": lambda a, b: a * b,
    "DIV": lambda a, b: a / b,
}


def registrar(host_nomes: str, meu_host: str, minha_porta: int) -> None:
    with socket.create_connection((host_nomes, 5000), timeout=5) as s:
        s.sendall(f"REGISTRAR calculadora {meu_host} {minha_porta}\n".encode())
        print(f"[replica-{minha_porta}] registro no serviço de nomes: {s.recv(100).decode().strip()}")


def atender(conexao: socket.socket, identidade: str) -> None:
    with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
        for linha in entrada:
            partes = linha.split()
            try:
                op, a, b = partes[0].upper(), float(partes[1]), float(partes[2])
                resposta = f"{OPERACOES[op](a, b)} (atendido por {identidade})"
            except (KeyError, IndexError, ValueError, ZeroDivisionError) as erro:
                resposta = f"ERRO {type(erro).__name__}"
            print(f"[{identidade}] {linha.strip()} -> {resposta}")
            conexao.sendall((resposta + "\n").encode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("porta", type=int)
    parser.add_argument("--host-nomes", default="127.0.0.1", help="IP do serviço de nomes")
    parser.add_argument("--meu-host", default="127.0.0.1", help="IP pelo qual os clientes me acham")
    args = parser.parse_args()

    identidade = f"replica-{args.porta}@{socket.gethostname()}"
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", args.porta))
    servidor.listen()
    registrar(args.host_nomes, args.meu_host, args.porta)
    print(f"[{identidade}] pronta")
    while True:
        conexao, _ = servidor.accept()
        threading.Thread(target=atender, args=(conexao, identidade), daemon=True).start()


if __name__ == "__main__":
    main()
