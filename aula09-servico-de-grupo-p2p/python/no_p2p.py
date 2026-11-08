"""
Aula 09: Paradigma PEER-TO-PEER (P2P) com busca por INUNDAÇÃO (estilo Gnutella).

Cada nó (peer) é ao mesmo tempo CLIENTE e SERVIDOR:
  * guarda alguns arquivos;
  * conhece só alguns vizinhos (não existe servidor central);
  * repassa as buscas aos vizinhos, diminuindo o TTL a cada salto.

    A --- B --- C
    |           |
    D --------- E     "quem tem aula09.pdf?" sai de A e se espalha pela rede

Protocolo de texto (uma linha por conexão TCP), igual ao NoP2P.java:
    BUSCA <id> <ttl> <arquivo> <host:porta_de_quem_perguntou>
    ACHEI <id> <arquivo> <host:porta_de_quem_tem>        (enviado direto a quem perguntou)

Executar a demonstração completa (5 nós no mesmo computador):
    python no_p2p.py demo
Executar um nó isolado:
    python no_p2p.py no 8101 --arquivos aula09.pdf musica.mp3 --vizinhos 127.0.0.1:8102
    (digite o nome de um arquivo para buscá-lo na rede)
"""

import argparse
import socket
import sys
import threading
import time
import uuid


class NoP2P:
    def __init__(self, porta: int, arquivos: list[str], vizinhos: list[str]) -> None:
        self.endereco = f"127.0.0.1:{porta}"
        self.porta, self.arquivos, self.vizinhos = porta, set(arquivos), vizinhos
        self.vistas: set[str] = set()      # ids de buscas já processadas (evita laços infinitos)
        self.trava = threading.Lock()

    # ---------- lado SERVIDOR do peer
    def iniciar(self) -> None:
        srv = socket.socket()
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", self.porta))
        srv.listen()
        threading.Thread(target=self._aceitar, args=(srv,), daemon=True).start()

    def _aceitar(self, srv) -> None:
        while True:
            c, _ = srv.accept()
            with c:
                linha = c.makefile("r", encoding="utf-8").readline().strip()
            threading.Thread(target=self._tratar, args=(linha,), daemon=True).start()

    def _tratar(self, linha: str) -> None:
        partes = linha.split(" ")
        if partes[0] == "BUSCA":
            _, id_busca, ttl, arquivo, origem = partes
            with self.trava:
                if id_busca in self.vistas:
                    return
                self.vistas.add(id_busca)
            if arquivo in self.arquivos:
                self._enviar(origem, f"ACHEI {id_busca} {arquivo} {self.endereco}")
            if int(ttl) > 1:                                  # repassa com TTL menor
                for v in self.vizinhos:
                    self._enviar(v, f"BUSCA {id_busca} {int(ttl) - 1} {arquivo} {origem}")
        elif partes[0] == "ACHEI":
            print(f"[{self.endereco}] '{partes[2]}' encontrado em {partes[3]}")

    # ---------- lado CLIENTE do peer
    def _enviar(self, destino: str, mensagem: str) -> None:
        host, porta = destino.split(":")
        try:
            with socket.create_connection((host, int(porta)), timeout=2) as s:
                s.sendall((mensagem + "\n").encode("utf-8"))
        except OSError:
            pass                                              # vizinho fora do ar: P2P tolera

    def buscar(self, arquivo: str, ttl: int = 4) -> None:
        id_busca = uuid.uuid4().hex[:8]
        self.vistas.add(id_busca)
        print(f"[{self.endereco}] buscando '{arquivo}' (TTL={ttl})...")
        for v in self.vizinhos:
            self._enviar(v, f"BUSCA {id_busca} {ttl} {arquivo} {self.endereco}")


def demo() -> None:
    # Topologia:  A(8101) - B(8102) - C(8103)
    #             |                    |
    #             D(8104) ----------- E(8105)
    rede = {
        8101: (["notas.txt"], [8102, 8104]),
        8102: (["aula08.pdf"], [8101, 8103]),
        8103: (["aula09.pdf", "musica.mp3"], [8102, 8105]),
        8104: ([], [8101, 8105]),
        8105: (["aula09.pdf"], [8103, 8104]),
    }
    nos = {}
    for porta, (arqs, viz) in rede.items():
        nos[porta] = NoP2P(porta, arqs, [f"127.0.0.1:{v}" for v in viz])
        nos[porta].iniciar()
    time.sleep(0.5)
    nos[8101].buscar("aula09.pdf")      # deve achar em C e em E
    time.sleep(1)
    nos[8101].buscar("musica.mp3", ttl=1)   # TTL baixo: não chega até C
    time.sleep(1)
    print("(com TTL=1 a busca só alcança os vizinhos diretos, por isso nada foi achado)")
    nos[8101].buscar("musica.mp3", ttl=3)
    time.sleep(1)


if __name__ == "__main__":
    if sys.argv[1:2] == ["demo"]:
        demo()
    else:
        p = argparse.ArgumentParser()
        p.add_argument("modo")
        p.add_argument("porta", type=int)
        p.add_argument("--arquivos", nargs="*", default=[])
        p.add_argument("--vizinhos", nargs="*", default=[])
        a = p.parse_args()
        no = NoP2P(a.porta, a.arquivos, a.vizinhos)
        no.iniciar()
        print(f"Nó {no.endereco} com {sorted(no.arquivos)}; vizinhos {no.vizinhos}")
        print("Digite o nome de um arquivo para buscar:")
        for linha in sys.stdin:
            if linha.strip():
                no.buscar(linha.strip())
