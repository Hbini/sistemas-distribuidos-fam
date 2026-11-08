"""
Aula 02: Exemplo 2, o mesmo cálculo de primos agora DISTRIBUÍDO pela rede.

Arquitetura (mestre/trabalhador):

        +-------------+     pedaço 1     +---------------+
        |             | ---------------> | trabalhador A |
        | COORDENADOR |     pedaço 2     +---------------+
        |   (mestre)  | ---------------> | trabalhador B |
        |             | <--- parciais -- +---------------+
        +-------------+

Diferença para o exemplo paralelo:
  * Cada trabalhador é um PROCESSO INDEPENDENTE, que pode estar em OUTRA
    MÁQUINA. Não há memória compartilhada: tudo é trocado por MENSAGENS (TCP).
  * Isso é um sistema distribuído: componentes autônomos que cooperam pela rede.

Como executar (abra 3 terminais):
    Terminal 1: python coordenador_trabalhadores.py trabalhador 6001
    Terminal 2: python coordenador_trabalhadores.py trabalhador 6002
    Terminal 3: python coordenador_trabalhadores.py coordenador 127.0.0.1:6001 127.0.0.1:6002

Para usar máquinas diferentes no laboratório, troque 127.0.0.1 pelo IP de cada
máquina que está rodando um trabalhador (descubra com ipconfig ou ip a).
"""

import json
import socket
import sys
import threading
import time


def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def enviar_json(sock: socket.socket, obj: dict) -> None:
    """Envia um objeto como JSON terminado por quebra de linha (protocolo simples)."""
    sock.sendall((json.dumps(obj) + "\n").encode("utf-8"))


def receber_json(sock: socket.socket) -> dict:
    """Lê bytes até encontrar a quebra de linha e converte de volta para dict."""
    dados = b""
    while not dados.endswith(b"\n"):
        parte = sock.recv(4096)
        if not parte:
            raise ConnectionError("conexão encerrada pelo outro lado")
        dados += parte
    return json.loads(dados.decode("utf-8"))


# ---------------------------------------------------------------- trabalhador
def trabalhador(porta: int) -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", porta))
    servidor.listen()
    print(f"[trabalhador:{porta}] aguardando tarefas...")
    while True:
        conexao, endereco = servidor.accept()
        with conexao:
            tarefa = receber_json(conexao)
            inicio, fim = tarefa["inicio"], tarefa["fim"]
            print(f"[trabalhador:{porta}] recebi [{inicio}, {fim}) de {endereco[0]}")
            t0 = time.perf_counter()
            total = sum(1 for n in range(inicio, fim) if eh_primo(n))
            enviar_json(conexao, {"primos": total, "tempo": time.perf_counter() - t0,
                                  "host": socket.gethostname()})
            print(f"[trabalhador:{porta}] devolvi {total} primos")


# ---------------------------------------------------------------- coordenador
def coordenador(enderecos: list[str]) -> None:
    limite = 2_000_000
    n = len(enderecos)
    tamanho = limite // n
    resultados: list[dict] = [{}] * n

    def despachar(i: int, endereco: str) -> None:
        host, porta = endereco.split(":")
        inicio = i * tamanho
        fim = limite if i == n - 1 else (i + 1) * tamanho
        with socket.create_connection((host, int(porta)), timeout=120) as s:
            enviar_json(s, {"inicio": inicio, "fim": fim})
            resultados[i] = receber_json(s)

    t0 = time.perf_counter()
    # Uma thread por trabalhador: as tarefas são enviadas ao mesmo tempo.
    threads = [threading.Thread(target=despachar, args=(i, e)) for i, e in enumerate(enderecos)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total = sum(r["primos"] for r in resultados)

    for e, r in zip(enderecos, resultados):
        print(f"  {e:<20} host={r['host']:<15} primos={r['primos']:<7} tempo={r['tempo']:.2f}s")
    print(f"\nTotal de primos: {total}  (tempo total {time.perf_counter() - t0:.2f}s)")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "trabalhador":
        trabalhador(int(sys.argv[2]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "coordenador":
        coordenador(sys.argv[2:])
    else:
        print(__doc__)
