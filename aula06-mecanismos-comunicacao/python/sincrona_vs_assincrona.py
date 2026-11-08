"""
Aula 06: Comunicação SÍNCRONA x ASSÍNCRONA e TRANSIENTE x PERSISTENTE.

Tudo acontece em um único programa (com threads) para ficar fácil de observar.

  * Síncrona  : o remetente fica BLOQUEADO até receber a resposta.
  * Assíncrona: o remetente entrega a mensagem e CONTINUA trabalhando.
  * Transiente: se o receptor não estiver ativo, a mensagem se perde.
  * Persistente: a mensagem fica GUARDADA (fila) até o receptor voltar.

Executar: python sincrona_vs_assincrona.py
"""

import queue
import threading
import time


def servico_lento(pedido: str) -> str:
    time.sleep(1)                       # o "servidor" leva 1 s para responder
    return f"resposta para {pedido}"


print("=== 1. SÍNCRONA: o cliente espera cada resposta ===")
t0 = time.perf_counter()
for i in range(3):
    print("  ", servico_lento(f"pedido {i}"))
print(f"   tempo total: {time.perf_counter() - t0:.1f} s (3 x 1 s, o cliente ficou parado)\n")

print("=== 2. ASSÍNCRONA: o cliente envia e segue trabalhando ===")
t0 = time.perf_counter()
respostas: list[str] = []
threads = [threading.Thread(target=lambda p=f"pedido {i}": respostas.append(servico_lento(p))) for i in range(3)]
for t in threads:
    t.start()
print("   cliente: enviei os 3 pedidos e estou fazendo outra coisa...")
for t in threads:
    t.join()
print("  ", respostas)
print(f"   tempo total: {time.perf_counter() - t0:.1f} s\n")

print("=== 3. PERSISTENTE: fila guarda as mensagens enquanto o receptor está desligado ===")
fila: queue.Queue[str] = queue.Queue()
for i in range(3):
    fila.put(f"e-mail {i}")
    print(f"   remetente enviou e-mail {i} (receptor ainda DESLIGADO)")
print("   ... 2 segundos depois o receptor liga ...")
time.sleep(2)
while not fila.empty():
    print(f"   receptor leu: {fila.get()}")
print("   Nada se perdeu: é assim que funcionam e-mail, RabbitMQ e Kafka (Aula 11).")
