"""
Aula 02: Sistemas centralizados, distribuídos, paralelos e de alto desempenho
Exemplo 1: o mesmo trabalho feito de forma SEQUENCIAL e de forma PARALELA.

Ideia central:
  * Sequencial: um único processador faz todas as tarefas, uma após a outra.
  * Paralelo: várias unidades de processamento (núcleos) dividem o trabalho
    e executam ao mesmo tempo, na MESMA máquina, com memória local.
  * Distribuído: o trabalho é dividido entre MÁQUINAS diferentes, que se
    comunicam pela rede (veja o exemplo coordenador_trabalhadores.py).

Tarefa usada: contar quantos números primos existem em um intervalo grande.
É uma tarefa "CPU bound" (gasta processador), ótima para ver o ganho do paralelismo.

Como executar:
    python sequencial_vs_paralelo.py
    python sequencial_vs_paralelo.py 4        (força 4 processos)
"""

import os
import sys
import time
from multiprocessing import Pool


def eh_primo(n: int) -> bool:
    """Teste de primalidade simples (propositalmente "pesado")."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def contar_primos(intervalo: tuple[int, int]) -> int:
    """Conta os primos em [inicio, fim). Cada processo recebe um pedaço."""
    inicio, fim = intervalo
    return sum(1 for n in range(inicio, fim) if eh_primo(n))


def dividir(limite: int, partes: int) -> list[tuple[int, int]]:
    """Divide o intervalo [0, limite) em 'partes' pedaços do mesmo tamanho."""
    tamanho = limite // partes
    pedacos = []
    for i in range(partes):
        inicio = i * tamanho
        fim = limite if i == partes - 1 else (i + 1) * tamanho
        pedacos.append((inicio, fim))
    return pedacos


def main() -> None:
    limite = 2_000_000
    processos = int(sys.argv[1]) if len(sys.argv) > 1 else (os.cpu_count() or 2)

    print(f"Contando primos de 0 até {limite:,}".replace(",", "."))
    print(f"Núcleos disponíveis nesta máquina: {os.cpu_count()}\n")

    # 1) Execução sequencial: um processo faz tudo
    t0 = time.perf_counter()
    total_seq = contar_primos((0, limite))
    t_seq = time.perf_counter() - t0
    print(f"[SEQUENCIAL] {total_seq} primos em {t_seq:.2f} s")

    # 2) Execução paralela: o intervalo é dividido entre vários processos
    t0 = time.perf_counter()
    with Pool(processes=processos) as pool:
        parciais = pool.map(contar_primos, dividir(limite, processos))
    total_par = sum(parciais)
    t_par = time.perf_counter() - t0
    print(f"[PARALELO ] {total_par} primos em {t_par:.2f} s com {processos} processos")
    print(f"            resultados parciais por processo: {parciais}")

    # 3) Métricas clássicas de alto desempenho
    speedup = t_seq / t_par
    eficiencia = speedup / processos
    print(f"\nSpeedup    = T_seq / T_par = {speedup:.2f}x")
    print(f"Eficiência = Speedup / p   = {eficiencia:.0%}")
    print("\nObservação: o speedup quase nunca chega a p, porque existe custo para")
    print("criar processos, dividir o trabalho e juntar os resultados (overhead).")


if __name__ == "__main__":
    # O "if __name__" é obrigatório com multiprocessing no Windows e no macOS.
    main()
