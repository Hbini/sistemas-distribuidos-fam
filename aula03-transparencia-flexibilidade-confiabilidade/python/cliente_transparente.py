"""
Aula 03: Cliente com TRANSPARÊNCIA de localização, replicação e falha.

O que o usuário vê: "calcular(SOMA, 2, 3) = 5".
O que acontece por baixo (escondido pela função calcular):
  1. pergunta ao serviço de nomes onde está a "calculadora"     (localização)
  2. recebe uma LISTA de réplicas                                (replicação)
  3. tenta a primeira; se ela não responder, tenta a próxima     (falha)

Como executar (depois de subir servico_nomes.py e 2 ou 3 réplicas):
    python cliente_transparente.py
Durante a execução, derrube uma réplica com Ctrl+C e veja o cliente continuar.
"""

import random
import socket
import time

HOST_NOMES = "127.0.0.1"


def resolver(nome: str) -> list[str]:
    with socket.create_connection((HOST_NOMES, 5000), timeout=3) as s:
        s.sendall(f"RESOLVER {nome}\n".encode())
        resposta = s.recv(4096).decode().strip()
    return [] if resposta == "VAZIO" else resposta.split(",")


def calcular(operacao: str, a: float, b: float) -> str:
    """Para quem chama, parece uma função local. Toda a distribuição fica aqui dentro."""
    replicas = resolver("calculadora")
    random.shuffle(replicas)  # espalha a carga entre as réplicas
    for endereco in replicas:
        host, porta = endereco.split(":")
        try:
            with socket.create_connection((host, int(porta)), timeout=2) as s:
                s.sendall(f"{operacao} {a} {b}\n".encode())
                return s.recv(4096).decode().strip()
        except OSError:
            # A réplica está fora do ar. O usuário não fica sabendo: tentamos a próxima.
            print(f"   (aviso interno: {endereco} não respondeu, tentando outra réplica)")
    raise RuntimeError("nenhuma réplica disponível: o serviço está totalmente fora do ar")


def main() -> None:
    contas = [("SOMA", 2, 3), ("MULT", 4, 5), ("SUB", 10, 7), ("DIV", 9, 3)]
    for i in range(20):
        op, a, b = contas[i % len(contas)]
        try:
            print(f"{op} {a} {b} = {calcular(op, a, b)}")
        except RuntimeError as erro:
            print(f"FALHA TOTAL: {erro}")
        time.sleep(1)


if __name__ == "__main__":
    main()
