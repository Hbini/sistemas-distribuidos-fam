"""
Aula 05: Microsserviço CATÁLOGO (Python, porta 8001).

Responsabilidade ÚNICA: saber quais produtos existem e quanto custam.
Ele tem seus PRÓPRIOS dados (o dicionário PRODUTOS) e ninguém acessa esses
dados diretamente: só pela API HTTP/JSON abaixo. Isso é um microsserviço.

Rotas:
    GET /saude              -> {"status": "ok"}       (health check)
    GET /produtos           -> lista de produtos
    GET /produtos/<id>      -> um produto ou 404

Executar: python servico_catalogo.py
Testar:   curl http://localhost:8001/produtos
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = int(os.environ.get("PORTA", 8001))

PRODUTOS = {
    1: {"id": 1, "nome": "Coxinha", "preco": 7.50},
    2: {"id": 2, "nome": "Pastel de queijo", "preco": 9.00},
    3: {"id": 3, "nome": "Suco de laranja", "preco": 6.00},
    4: {"id": 4, "nome": "Pão de queijo", "preco": 4.50},
}


class Catalogo(BaseHTTPRequestHandler):
    def responder(self, status: int, corpo) -> None:
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self) -> None:
        partes = [p for p in self.path.split("/") if p]
        if partes == ["saude"]:
            self.responder(200, {"status": "ok", "servico": "catalogo"})
        elif partes == ["produtos"]:
            self.responder(200, list(PRODUTOS.values()))
        elif len(partes) == 2 and partes[0] == "produtos" and partes[1].isdigit():
            produto = PRODUTOS.get(int(partes[1]))
            self.responder(200, produto) if produto else self.responder(404, {"erro": "produto não existe"})
        else:
            self.responder(404, {"erro": "rota não encontrada"})

    def log_message(self, formato, *args) -> None:
        print(f"[catalogo] {self.command} {self.path}")


if __name__ == "__main__":
    print(f"[catalogo] ouvindo na porta {PORTA}")
    ThreadingHTTPServer(("0.0.0.0", PORTA), Catalogo).serve_forever()
