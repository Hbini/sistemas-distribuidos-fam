"""
Aula 05: Microsserviço PEDIDOS (Python, porta 8003).

Este serviço COMPÕE os outros dois:
    1. pergunta ao CATÁLOGO o preço do produto      (GET  /produtos/<id>)
    2. pede ao ESTOQUE para baixar a quantidade     (POST /estoque/<id>/baixar)
    3. registra o pedido nos SEUS próprios dados

Note que ele não sabe em que linguagem os outros serviços foram escritos
(o estoque é Java!). Só conhece as URLs e o formato JSON.

Rotas:
    GET  /saude
    GET  /pedidos
    POST /pedidos   corpo: {"produto_id": 1, "quantidade": 2}

Variáveis de ambiente (usadas no Docker):
    CATALOGO_URL (padrão http://localhost:8001)
    ESTOQUE_URL  (padrão http://localhost:8002)
"""

import json
import os
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = int(os.environ.get("PORTA", 8003))
CATALOGO_URL = os.environ.get("CATALOGO_URL", "http://localhost:8001")
ESTOQUE_URL = os.environ.get("ESTOQUE_URL", "http://localhost:8002")

pedidos: list[dict] = []
trava = threading.Lock()


def chamar(metodo: str, url: str, corpo: dict | None = None) -> tuple[int, dict]:
    """Faz uma chamada HTTP a outro microsserviço e devolve (status, json)."""
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as erro:
        return erro.code, json.loads(erro.read() or b"{}")
    except urllib.error.URLError:
        return 503, {"erro": f"serviço indisponível: {url}"}


class Pedidos(BaseHTTPRequestHandler):
    def responder(self, status: int, corpo) -> None:
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self) -> None:
        if self.path == "/saude":
            self.responder(200, {"status": "ok", "servico": "pedidos"})
        elif self.path == "/pedidos":
            with trava:
                self.responder(200, pedidos)
        else:
            self.responder(404, {"erro": "rota não encontrada"})

    def do_POST(self) -> None:
        if self.path != "/pedidos":
            return self.responder(404, {"erro": "rota não encontrada"})
        tamanho = int(self.headers.get("Content-Length", 0))
        entrada = json.loads(self.rfile.read(tamanho) or b"{}")
        pid, qtd = entrada.get("produto_id"), int(entrada.get("quantidade", 1))

        status, produto = chamar("GET", f"{CATALOGO_URL}/produtos/{pid}")          # passo 1
        if status != 200:
            return self.responder(status, {"erro": "catálogo", "detalhe": produto})

        status, estoque = chamar("POST", f"{ESTOQUE_URL}/estoque/{pid}/baixar",     # passo 2
                                 {"quantidade": qtd})
        if status != 200:
            return self.responder(status, {"erro": "estoque", "detalhe": estoque})

        with trava:                                                                 # passo 3
            pedido = {"numero": len(pedidos) + 1, "produto": produto["nome"], "quantidade": qtd,
                      "total": round(produto["preco"] * qtd, 2), "estoque_restante": estoque["restante"]}
            pedidos.append(pedido)
        self.responder(201, pedido)

    def log_message(self, formato, *args) -> None:
        print(f"[pedidos] {self.command} {self.path}")


if __name__ == "__main__":
    print(f"[pedidos] porta {PORTA} | catálogo={CATALOGO_URL} | estoque={ESTOQUE_URL}")
    ThreadingHTTPServer(("0.0.0.0", PORTA), Pedidos).serve_forever()
