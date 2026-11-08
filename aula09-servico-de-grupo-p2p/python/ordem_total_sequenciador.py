"""
Aula 09: SINCRONIZAÇÃO em serviço de grupo: ORDEM TOTAL com SEQUENCIADOR.

Problema: duas pessoas enviam ao grupo quase ao mesmo tempo. Por causa dos
atrasos diferentes da rede, cada membro pode receber as mensagens em ORDEM
DIFERENTE. Em uma réplica de banco de dados isso é desastroso:

    Réplica 1: "saldo = 100" e depois "saldo += 10"  -> 110
    Réplica 2: "saldo += 10" e depois "saldo = 100"  -> 100   (réplicas divergiram!)

Solução clássica: um SEQUENCIADOR numera todas as mensagens (1, 2, 3...).
Cada membro guarda as que chegam fora de ordem e só ENTREGA à aplicação
na ordem dos números. Resultado: todos aplicam as operações na mesma ordem.

A rede é SIMULADA com threads e atrasos aleatórios, para o efeito ser visível.
Executar: python ordem_total_sequenciador.py
"""

import heapq
import random
import threading
import time

OPERACOES = [("Ana", "saldo = 100"), ("Bruno", "saldo += 10"), ("Carla", "saldo *= 2")]


def aplicar(saldo: int, op: str) -> int:
    if op.startswith("saldo = "):
        return int(op.split("= ")[1])
    if op.startswith("saldo += "):
        return saldo + int(op.split("+= ")[1])
    return saldo * int(op.split("*= ")[1])


class Membro:
    def __init__(self, nome: str, com_sequenciador: bool) -> None:
        self.nome, self.com_seq = nome, com_sequenciador
        self.saldo, self.entregues = 0, []
        self.proximo = 1                  # próximo número de sequência esperado
        self.pendentes: list = []         # mensagens que chegaram adiantadas
        self.trava = threading.Lock()

    def receber(self, seq: int, op: str) -> None:
        with self.trava:
            if not self.com_seq:          # sem sequenciador: entrega na ordem em que chegou
                self._entregar(op)
                return
            heapq.heappush(self.pendentes, (seq, op))
            while self.pendentes and self.pendentes[0][0] == self.proximo:
                _, pronta = heapq.heappop(self.pendentes)
                self._entregar(pronta)
                self.proximo += 1

    def _entregar(self, op: str) -> None:
        self.saldo = aplicar(self.saldo, op)
        self.entregues.append(op)


def rede_com_atraso(membros, seq, op) -> None:
    """Envia a mensagem a cada membro com um atraso aleatório (rede real)."""
    for m in membros:
        atraso = random.uniform(0, 0.3)
        threading.Timer(atraso, m.receber, args=(seq, op)).start()


def experimento(com_sequenciador: bool) -> None:
    membros = [Membro(f"réplica {i}", com_sequenciador) for i in range(1, 5)]
    numero = 0
    for remetente, op in OPERACOES:
        numero += 1                       # o sequenciador atribui o número global
        rede_com_atraso(membros, numero, op)
        time.sleep(0.05)
    time.sleep(0.6)
    titulo = "COM sequenciador (ordem total)" if com_sequenciador else "SEM sequenciador"
    print(f"\n=== {titulo} ===")
    for m in membros:
        print(f"{m.nome}: saldo final = {m.saldo:>4} | ordem: {m.entregues}")
    saldos = {m.saldo for m in membros}
    print("Resultado:", "todas as réplicas IGUAIS" if len(saldos) == 1 else "réplicas DIVERGIRAM!")


if __name__ == "__main__":
    random.seed()
    experimento(com_sequenciador=False)
    experimento(com_sequenciador=True)
