"""
Aula 07: Paradigma de MEMÓRIA COMPARTILHADA (e seu maior perigo: condição de corrida).

4 processos incrementam o MESMO contador 50.000 vezes cada. O resultado
correto é 200.000. Sem sincronização, incrementos se perdem, porque
"contador += 1" na verdade são 3 passos: LER, SOMAR, ESCREVER.

    processo A lê 10        processo B lê 10
    A escreve 11            B escreve 11     -> um incremento sumiu!

Executar: python memoria_compartilhada.py
"""

from multiprocessing import Lock, Process, Value

N = 50_000


def sem_trava(contador) -> None:
    for _ in range(N):
        contador.value += 1                 # leitura + soma + escrita NÃO atômicas


def com_trava(contador, trava) -> None:
    for _ in range(N):
        with trava:                         # só um processo por vez na seção crítica
            contador.value += 1


def rodar(alvo, *args) -> None:
    processos = [Process(target=alvo, args=args) for _ in range(4)]
    for p in processos:
        p.start()
    for p in processos:
        p.join()


if __name__ == "__main__":
    c1 = Value("i", 0, lock=False)          # memória compartilhada SEM proteção
    rodar(sem_trava, c1)
    print(f"Sem trava : {c1.value:>7} (esperado 200000) -> {200000 - c1.value} incrementos perdidos")

    c2 = Value("i", 0, lock=False)
    rodar(com_trava, c2, Lock())
    print(f"Com trava : {c2.value:>7} (esperado 200000)")
    print("\nEm um sistema DISTRIBUÍDO não existe essa memória comum: os processos")
    print("estão em máquinas diferentes. Por isso usamos TROCA DE MENSAGENS e")
    print("algoritmos de exclusão mútua distribuída (Aula 12).")
