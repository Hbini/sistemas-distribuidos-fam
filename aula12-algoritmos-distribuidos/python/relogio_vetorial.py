"""
Aula 12: Relógios VETORIAIS: detectam CAUSALIDADE e CONCORRÊNCIA.

Cada processo i guarda um vetor V com uma posição por processo.
  * evento local ou envio: V[i] += 1
  * a mensagem leva o vetor inteiro
  * ao receber W: V[k] = max(V[k], W[k]) para todo k; depois V[i] += 1

Comparação de dois eventos a e b:
  a -> b  (a aconteceu antes) se V(a) <= V(b) em todas as posições e são diferentes
  a || b  (concorrentes) se nenhum é <= ao outro

Executar: python relogio_vetorial.py
"""

N = 3


class Processo:
    def __init__(self, i: int) -> None:
        self.i, self.v = i, [0] * N

    def local(self, nome: str) -> tuple[str, list[int]]:
        self.v[self.i] += 1
        print(f"P{self.i + 1}: {nome:<4} {self.v}")
        return nome, list(self.v)

    def enviar(self, nome: str) -> tuple[str, list[int]]:
        return self.local(nome)

    def receber(self, nome: str, w: list[int]) -> tuple[str, list[int]]:
        self.v = [max(a, b) for a, b in zip(self.v, w)]
        self.v[self.i] += 1
        print(f"P{self.i + 1}: {nome:<4} {self.v}   (recebeu {w})")
        return nome, list(self.v)


def relacao(a: tuple[str, list[int]], b: tuple[str, list[int]]) -> str:
    (na, va), (nb, vb) = a, b
    if all(x <= y for x, y in zip(va, vb)) and va != vb:
        return f"{na} -> {nb}  ({na} aconteceu antes de {nb})"
    if all(y <= x for x, y in zip(va, vb)) and va != vb:
        return f"{nb} -> {na}"
    return f"{na} || {nb}  (CONCORRENTES: nenhum causou o outro)"


p = [Processo(0), Processo(1), Processo(2)]
a = p[0].local("a")
b = p[0].enviar("b")                 # P1 envia para P2
c = p[1].local("c")
d = p[1].receber("d", b[1])
e = p[2].local("e")
f = p[1].enviar("f")                 # P2 envia para P3
g = p[2].receber("g", f[1])

print()
for x, y in [(a, d), (c, e), (b, g), (e, g), (a, e)]:
    print(relacao(x, y))
print("\nCom Lamport, 'c' e 'e' teriam números, mas não daria para saber que são concorrentes.")
