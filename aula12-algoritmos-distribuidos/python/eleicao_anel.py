"""
Aula 12: Eleição de líder em ANEL (algoritmo de Chang e Roberts, simplificado).

Os processos formam um anel lógico; cada um só conversa com o sucessor.
  1. Quem detecta a falha envia ELEIÇÃO[lista] ao sucessor vivo, com seu id.
  2. Cada processo acrescenta o próprio id e repassa.
  3. Quando a mensagem volta ao iniciador, o maior id da lista é o líder;
     uma mensagem COORDENADOR dá mais uma volta avisando todos.

Executar: python eleicao_anel.py
"""

anel = [3, 6, 1, 5, 2, 4]        # ordem física do anel (não precisa ser crescente)
caidos = {6}                     # o antigo líder (6) caiu
iniciador = 1

print(f"Anel: {' -> '.join(map(str, anel))} -> (volta ao {anel[0]}) | caído: {caidos}\n")


def sucessor_vivo(pid: int) -> int:
    i = anel.index(pid)
    for passo in range(1, len(anel) + 1):
        candidato = anel[(i + passo) % len(anel)]
        if candidato not in caidos:
            return candidato
        print(f"   P{pid}: P{candidato} não responde, pulando para o próximo")
    raise RuntimeError("todos caíram")


lista = [iniciador]
atual = iniciador
mensagens = 0
while True:
    prox = sucessor_vivo(atual)
    mensagens += 1
    print(f"P{atual} -> P{prox}: ELEIÇÃO{lista}")
    if prox == iniciador:
        break
    lista.append(prox)
    atual = prox

lider = max(lista)
print(f"\nA mensagem voltou ao P{iniciador}. Maior id da lista {lista}: P{lider} é o novo líder.")
atual = iniciador
while True:
    prox = sucessor_vivo(atual)
    mensagens += 1
    print(f"P{atual} -> P{prox}: COORDENADOR({lider})")
    if prox == iniciador:
        break
    atual = prox
print(f"\nTotal de mensagens: {mensagens} (2 voltas no anel de {len(anel) - len(caidos)} processos vivos)")
