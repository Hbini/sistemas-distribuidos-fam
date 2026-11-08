"""
Aula 04: Lei de Amdahl e Lei de Gustafson, em números e em gráfico de texto.

Amdahl (problema de tamanho FIXO):
    Speedup(p) = 1 / ( s + (1 - s) / p )
    s = fração do programa que é obrigatoriamente sequencial
    p = número de processadores
    Limite quando p tende ao infinito: 1 / s

Gustafson (problema que CRESCE junto com o número de processadores):
    Speedup(p) = p - s * (p - 1)

Como executar:
    python amdahl.py
    python amdahl.py 0.05       (testa com 5% sequencial)
"""

import sys


def amdahl(s: float, p: int) -> float:
    return 1 / (s + (1 - s) / p)


def gustafson(s: float, p: int) -> float:
    return p - s * (p - 1)


def barra(valor: float, escala: float = 2.0) -> str:
    return "#" * int(valor * escala)


def main() -> None:
    fracoes = [float(sys.argv[1])] if len(sys.argv) > 1 else [0.05, 0.10, 0.25, 0.50]
    processadores = [1, 2, 4, 8, 16, 32, 64, 128]

    for s in fracoes:
        print(f"\n=== Parte sequencial s = {s:.0%}  (limite de Amdahl = {1 / s:.1f}x) ===")
        print(f"{'p':>4} | {'Amdahl':>7} | {'Gustafson':>9} | gráfico Amdahl")
        for p in processadores:
            a = amdahl(s, p)
            print(f"{p:>4} | {a:>6.2f}x | {gustafson(s, p):>8.2f}x | {barra(a)}")

    print("\nConclusão: com tamanho fixo, a parte sequencial limita o ganho (Amdahl).")
    print("Se o problema cresce junto com o cluster, o ganho continua (Gustafson).")
    print("Por isso escalabilidade horizontal funciona bem para MUITOS usuários, mas")
    print("não acelera indefinidamente UMA única tarefa com partes sequenciais.")


if __name__ == "__main__":
    main()
