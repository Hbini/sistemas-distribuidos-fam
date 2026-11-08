"""
Aula 05: API GATEWAY (Python, porta 8000).

Porta de entrada ÚNICA para os clientes. O cliente não precisa saber que
existem três serviços em três portas: ele fala só com o gateway, que
encaminha (faz proxy) para o serviço certo de acordo com o caminho.

    /api/catalogo/...  ->  CATALOGO_URL/...
    /api/estoque/...   ->  ESTOQUE_URL/...
    /api/pedidos...    ->  PEDIDOS_URL/pedidos...

É também o lugar natural para autenticação, limite de requisições e logs.
"""

import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = int(os.environ.get("PORTA", 8000))
ROTAS = {
    "catalogo": os.environ.get("CATALOGO_URL", "http://localhost:8001"),
    "estoque": os.environ.get("ESTOQUE_URL", "http://localhost:8002"),
    "pedidos": os.environ.get("PEDIDOS_URL", "http://localhost:8003"),
}


class Gateway(BaseHTTPRequestHandler):
    def encaminhar(self) -> None:
        partes = self.path.split("/", 3)          # ['', 'api', 'servico', 'resto']
        if len(partes) < 3 or partes[1] != "api" or partes[2] not in ROTAS:
            self.send_error(404, "Use /api/catalogo, /api/estoque ou /api/pedidos")
            return
        servico = partes[2]
        resto = partes[3] if len(partes) > 3 else ""
        if servico == "pedidos":
            resto = "pedidos" + ("/" + resto if resto else "")
        destino = f"{ROTAS[servico]}/{resto}"

        corpo = None
        if self.command == "POST":
            corpo = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(destino, data=corpo, method=self.command,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                status, dados = resp.status, resp.read()
        except urllib.error.HTTPError as erro:
            status, dados = erro.code, erro.read()
        except urllib.error.URLError:
            status, dados = 503, f'{{"erro": "{servico} fora do ar"}}'.encode()

        print(f"[gateway] {self.command} {self.path} -> {destino} ({status})")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    do_GET = encaminhar
    do_POST = encaminhar

    def log_message(self, formato, *args) -> None:
        pass


if __name__ == "__main__":
    print(f"[gateway] porta {PORTA} -> {ROTAS}")
    ThreadingHTTPServer(("0.0.0.0", PORTA), Gateway).serve_forever()
