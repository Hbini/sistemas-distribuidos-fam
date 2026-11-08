"""
Aula 12: Relógios lógicos de LAMPORT.

Não existe relógio global em um sistema distribuído. Lamport propôs um
contador por processo que respeita a relação "aconteceu antes" (->):

  Regra 1: antes de cada evento local ou envio, C = C + 1
  Regra 2: toda mensagem leva junto o valor C de quem enviou
  Regra 3: ao receber, C = max(C_local, C_mensagem) + 1

Garantia: se a -> b então C(a) < C(b). (A volta NÃO vale: C(a) < C(b) não
prova que a causou b. Para isso existem os relógios vetoriais.)

O roteiro abaixo é executado passo a passo para você conferir no quadro.
Executar: python relogio_lamport.py
"""


class Processo:
    def __init__(self, nome: str) -> None:
        self.nome, self.relogio = nome, 0

    def evento_local(self, descricao: str) -> None:
        self.relogio += 1                                      # regra 1
        print(f"{self.nome}: {descricao:<28} C={self.relogio}")

    def enviar(self, destino: str, msg: str) -> tuple[str, int]:
        self.relogio += 1                                      # regra 1
        print(f"{self.nome}: envia '{msg}' para {destino:<10} C={self.relogio}")
        return msg, self.relogio                               # regra 2

    def receber(self, mensagem: tuple[str, int]) -> None:
        msg, carimbo = mensagem
        antes = self.relogio
        self.relogio = max(self.relogio, carimbo) + 1          # regra 3
        print(f"{self.nome}: recebe '{msg}' (carimbo {carimbo})   "
              f"C = max({antes}, {carimbo}) + 1 = {self.relogio}")


p1, p2, p3 = Processo("P1"), Processo("P2"), Processo("P3")

# Roteiro (cada linha acontece depois da anterior no "tempo real")
p1.evento_local("calcula pedido")
m1 = p1.enviar("P2", "m1")
p3.evento_local("lê sensor")
p3.evento_local("grava log")
p3.evento_local("atualiza cache")
m2 = p3.enviar("P2", "m2")
p2.receber(m1)
p2.receber(m2)
p2.evento_local("processa dados")
m3 = p2.enviar("P1", "m3")
p1.receber(m3)

print("\nOrdem TOTAL (desempate pelo número do processo):")
print("Se dois eventos têm o mesmo C, vem antes o de menor número de processo,")
print("por exemplo (C=2, P1) antes de (C=2, P3). Assim todos concordam na ordem.")
