"""
Aula 12: Eleição de líder: algoritmo do VALENTÃO (Bully), Garcia-Molina 1982.

Regra: o processo VIVO com MAIOR identificador deve ser o coordenador.
  1. P percebe que o coordenador não responde (timeout).
  2. P envia ELEIÇÃO a todos com id MAIOR que o seu.
  3. Se ninguém responder OK, P vence e envia COORDENADOR a todos.
  4. Se alguém maior responder OK, P desiste e espera; o maior continua a eleição.

Simulação determinística (sem rede) para acompanhar mensagem por mensagem.
Executar: python eleicao_bully.py
          python eleicao_bully.py 7 3 2 5      (7 processos; caem 7 e 5; o 2 detecta)
"""

import sys


class Sistema:
    def __init__(self, n: int, caidos: set[int]) -> None:
        self.ids = list(range(1, n + 1))
        self.vivos = set(self.ids) - caidos
        self.coordenador = max(self.ids)
        self.mensagens = 0

    def eleicao(self, iniciador: int, nivel: int = 0) -> None:
        recuo = "   " * nivel
        maiores = [i for i in self.ids if i > iniciador]
        print(f"{recuo}P{iniciador} inicia eleição e envia ELEIÇÃO para {['P%d' % i for i in maiores] or 'ninguém'}")
        self.mensagens += len(maiores)
        responderam = [i for i in maiores if i in self.vivos]
        for i in maiores:
            if i not in self.vivos:
                print(f"{recuo}   P{i} não responde (está fora do ar)")
        if not responderam:
            self.coordenador = iniciador
            outros = [i for i in self.ids if i != iniciador and i in self.vivos]
            self.mensagens += len(outros)
            print(f"{recuo}>>> Ninguém maior respondeu. P{iniciador} é o NOVO COORDENADOR "
                  f"e envia COORDENADOR para {['P%d' % i for i in outros]}")
            return
        for i in responderam:
            print(f"{recuo}   P{i} responde OK para P{iniciador} (\"deixa comigo\")")
        self.mensagens += len(responderam)
        # Cada processo maior que respondeu inicia sua própria eleição.
        # Basta seguir o de menor id: os outros chegam ao mesmo resultado.
        self.eleicao(min(responderam), nivel + 1)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    detector = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    caidos = {int(x) for x in sys.argv[3:]} if len(sys.argv) > 3 else {n}
    s = Sistema(n, caidos)
    print(f"Processos: {s.ids} | coordenador atual: P{s.coordenador} | fora do ar: {sorted(caidos)}")
    print(f"P{detector} enviou uma requisição ao coordenador e não teve resposta (timeout).\n")
    s.eleicao(detector)
    print(f"\nResultado: coordenador = P{s.coordenador} | mensagens trocadas (aprox.): {s.mensagens}")
