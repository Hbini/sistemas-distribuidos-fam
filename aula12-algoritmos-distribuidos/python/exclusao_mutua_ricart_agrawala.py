"""
Aula 12: EXCLUSÃO MÚTUA DISTRIBUÍDA: algoritmo de Ricart e Agrawala (1981).

Problema: 3 caixas (processos em máquinas diferentes) querem imprimir na
MESMA impressora (seção crítica). Não há memória compartilhada nem trava comum.

Algoritmo (baseado em relógios de Lamport):
  * Quem quer entrar envia PEDIDO(carimbo, id) a todos e espera N-1 respostas OK.
  * Ao receber um PEDIDO, o processo responde OK na hora, a menos que:
      - esteja NA seção crítica, ou
      - também queira entrar e o SEU pedido seja mais antigo (menor carimbo;
        empate decidido pelo menor id).
    Nesses casos ele ADIA a resposta e só responde ao sair da seção crítica.
  * Custo: 2(N-1) mensagens por entrada.

A rede é simulada com filas e threads (cada processo tem sua "caixa de entrada").
Executar: python exclusao_mutua_ricart_agrawala.py
"""

import queue
import random
import threading
import time

N = 3
caixas = [queue.Queue() for _ in range(N)]   # "rede": caixa de entrada de cada processo
impressora_em_uso = threading.Event()        # só para PROVAR que nunca há 2 dentro ao mesmo tempo


class Processo(threading.Thread):
    def __init__(self, pid: int) -> None:
        super().__init__(daemon=True)
        self.pid, self.relogio = pid, 0
        self.estado = "LIBERADO"             # LIBERADO, QUERENDO, DENTRO
        self.meu_pedido = (0, pid)
        self.oks = 0
        self.adiados: list[int] = []
        self.trava = threading.Lock()
        self.liberou_ok = threading.Event()

    def enviar(self, destino: int, msg: tuple) -> None:
        time.sleep(random.uniform(0.01, 0.05))          # atraso de rede
        caixas[destino].put(msg)

    def run(self) -> None:                              # thread que recebe mensagens
        while True:
            tipo, carimbo, origem = caixas[self.pid].get()
            with self.trava:
                self.relogio = max(self.relogio, carimbo) + 1
                if tipo == "PEDIDO":
                    adiar = self.estado == "DENTRO" or (
                        self.estado == "QUERENDO" and self.meu_pedido < (carimbo, origem))
                    if adiar:
                        self.adiados.append(origem)
                        print(f"   P{self.pid} ADIA resposta a P{origem}")
                    else:
                        threading.Thread(target=self.enviar, args=(origem, ("OK", self.relogio, self.pid))).start()
                elif tipo == "OK":
                    self.oks += 1
                    if self.oks == N - 1:
                        self.liberou_ok.set()

    def usar_impressora(self, documento: str) -> None:
        with self.trava:
            self.estado, self.oks = "QUERENDO", 0
            self.relogio += 1
            self.meu_pedido = (self.relogio, self.pid)
            self.liberou_ok.clear()
        print(f"P{self.pid} quer imprimir '{documento}' com pedido {self.meu_pedido}")
        for outro in range(N):
            if outro != self.pid:
                threading.Thread(target=self.enviar, args=(outro, ("PEDIDO", self.meu_pedido[0], self.pid))).start()
        self.liberou_ok.wait()                          # espera N-1 OKs

        with self.trava:
            self.estado = "DENTRO"
        assert not impressora_em_uso.is_set(), "VIOLAÇÃO: dois processos na seção crítica!"
        impressora_em_uso.set()
        print(f">>> P{self.pid} ENTROU na seção crítica e imprime '{documento}'")
        time.sleep(0.3)
        impressora_em_uso.clear()
        print(f"<<< P{self.pid} SAIU da seção crítica")

        with self.trava:
            self.estado = "LIBERADO"
            adiados, self.adiados = self.adiados, []
        for outro in adiados:
            threading.Thread(target=self.enviar, args=(outro, ("OK", self.relogio, self.pid))).start()


processos = [Processo(i) for i in range(N)]
for p in processos:
    p.start()

documentos = ["boleto.pdf", "nota_fiscal.pdf", "relatorio.pdf"]
clientes = [threading.Thread(target=processos[i].usar_impressora, args=(documentos[i],)) for i in range(N)]
for c in clientes:
    c.start()                                           # os três pedem quase ao mesmo tempo
for c in clientes:
    c.join()
print("\nTodos imprimiram, um de cada vez, sem coordenador central.")
