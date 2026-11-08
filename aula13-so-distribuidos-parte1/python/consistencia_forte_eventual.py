"""
Aula 13: Replicação: consistência FORTE x EVENTUAL, e o teorema CAP.

Três réplicas de um saldo. A rede tem atraso de propagação.
  * FORTE   : a escrita só termina quando TODAS as réplicas confirmam.
              Leitura sempre atual, mas a escrita é lenta e, se uma réplica
              estiver inacessível (partição), a escrita é RECUSADA (escolhe C).
  * EVENTUAL: a escrita termina na réplica local e é propagada depois.
              Rápida e sempre disponível, mas por um tempo leituras em outras
              réplicas devolvem valor ANTIGO (escolhe A).

Executar: python consistencia_forte_eventual.py
"""

import threading
import time

ATRASO = 0.5        # tempo para uma atualização chegar a outra réplica


class Replica:
    def __init__(self, nome: str) -> None:
        self.nome, self.saldo, self.acessivel = nome, 100, True

    def aplicar(self, valor: int) -> bool:
        time.sleep(ATRASO)
        if not self.acessivel:
            return False
        self.saldo = valor
        return True


def escrita_forte(replicas, valor) -> None:
    """Duas fases (ideia do two-phase commit): primeiro pergunta se TODAS podem
    gravar; só se todas disserem sim, grava em todas. Assim nunca fica pela metade."""
    t0 = time.perf_counter()
    time.sleep(ATRASO)                                    # fase 1: PREPARAR
    if not all(r.acessivel for r in replicas):
        print(f"  escrita FORTE de {valor} RECUSADA: réplica inacessível (sacrifica disponibilidade)")
        return
    resultados = [None] * len(replicas)
    ths = [threading.Thread(target=lambda i=i, r=r: resultados.__setitem__(i, r.aplicar(valor)))
           for i, r in enumerate(replicas)]
    for t in ths:                                         # fase 2: CONFIRMAR
        t.start()
    for t in ths:
        t.join()
    print(f"  escrita FORTE de {valor} confirmada por todas em {time.perf_counter() - t0:.1f}s")


def escrita_eventual(replicas, valor) -> None:
    t0 = time.perf_counter()
    replicas[0].saldo = valor                          # grava só na local
    for r in replicas[1:]:
        threading.Thread(target=r.aplicar, args=(valor,), daemon=True).start()   # propaga depois
    print(f"  escrita EVENTUAL de {valor} confirmada em {time.perf_counter() - t0:.3f}s (só local)")


def ler(replicas) -> str:
    return "  leituras: " + ", ".join(f"{r.nome}={r.saldo}" for r in replicas)


print("=== Consistência FORTE ===")
reps = [Replica("R1"), Replica("R2"), Replica("R3")]
escrita_forte(reps, 150)
print(ler(reps))

print("\n=== Consistência EVENTUAL ===")
reps = [Replica("R1"), Replica("R2"), Replica("R3")]
escrita_eventual(reps, 150)
print(ler(reps), " <- logo após a escrita (R2 e R3 desatualizadas!)")
time.sleep(ATRASO + 0.2)
print(ler(reps), " <- depois da propagação (convergiram)")

print("\n=== PARTIÇÃO de rede (R3 isolada): o dilema CAP ===")
reps = [Replica("R1"), Replica("R2"), Replica("R3")]
reps[2].acessivel = False
escrita_forte(reps, 200)
print(ler(reps), " (C: todas iguais, mas o cliente recebeu erro)")
escrita_eventual(reps, 200)
time.sleep(ATRASO + 0.2)
print(ler(reps), " (A: respondeu, mas R3 diverge até a rede voltar)")
