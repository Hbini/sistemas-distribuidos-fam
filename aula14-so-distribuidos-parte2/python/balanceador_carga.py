"""
Aula 14: Escalonamento / BALANCEAMENTO DE CARGA entre nós de um SOD.

200 tarefas com durações variadas são distribuídas para 4 servidores com
capacidades diferentes (um deles é 2x mais lento). Três políticas:
  * aleatória
  * round robin (um para cada, em rodízio)
  * menor carga (envia para quem vai ficar livre primeiro)

Medimos o MAKESPAN: o instante em que a última tarefa termina.
Executar: python balanceador_carga.py
"""
import random

random.seed(42)
TAREFAS = [random.choice([1, 1, 1, 2, 2, 5, 10]) for _ in range(200)]   # duração em segundos
VELOCIDADE = {"srv-1": 1.0, "srv-2": 1.0, "srv-3": 1.0, "srv-4": 0.5}  # srv-4 é mais lento


def simular(politica: str) -> tuple[float, dict]:
    livre_em = {s: 0.0 for s in VELOCIDADE}
    contagem = {s: 0 for s in VELOCIDADE}
    nomes = list(VELOCIDADE)
    for i, duracao in enumerate(TAREFAS):
        if politica == "aleatória":
            s = random.choice(nomes)
        elif politica == "round robin":
            s = nomes[i % len(nomes)]
        else:  # menor carga: escolhe o servidor que terminaria esta tarefa mais cedo
            s = min(nomes, key=lambda n: livre_em[n] + duracao / VELOCIDADE[n])
        livre_em[s] += duracao / VELOCIDADE[s]
        contagem[s] += duracao              # soma da duração das tarefas recebidas
    return max(livre_em.values()), contagem


print(f"{len(TAREFAS)} tarefas, soma das durações = {sum(TAREFAS)} s\n")
for politica in ["aleatória", "round robin", "menor carga"]:
    makespan, contagem = simular(politica)
    print(f"{politica:<12} makespan = {makespan:6.1f} s   trabalho (s) por servidor: {contagem}")
print("\nA política 'menor carga' dá MENOS trabalho ao servidor lento (srv-4) e termina antes.")
print("Ela exige INFORMAÇÃO sobre o estado dos nós, o que custa mensagens em um sistema real.")
