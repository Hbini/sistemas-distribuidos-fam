"""
Aula 11: Middleware para HETEROGENEIDADE: JSON-RPC 2.0 sobre HTTP.

O servidor é Python; o cliente pode ser Java (ClienteJsonRpc.java), JavaScript,
C#... Todos combinam o mesmo formato padronizado (especificação JSON-RPC 2.0):

    pedido : {"jsonrpc": "2.0", "method": "converter", "params": [10, "USD"], "id": 1}
    reposta: {"jsonrpc": "2.0", "result": 54.3, "id": 1}

Executar: python jsonrpc_servidor.py
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

COTACOES = {"USD": 5.43, "EUR": 5.87, "BRL": 1.0}   # valores fictícios para a aula


def converter(valor: float, moeda: str) -> float:
    return round(valor * COTACOES[moeda], 2)


def moedas() -> list:
    return sorted(COTACOES)


METODOS = {"converter": converter, "moedas": moedas}


class JsonRpc(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        pedido = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        resposta = {"jsonrpc": "2.0", "id": pedido.get("id")}
        try:
            resposta["result"] = METODOS[pedido["method"]](*pedido.get("params", []))
        except KeyError as e:
            resposta["error"] = {"code": -32601, "message": f"método ou moeda inexistente: {e}"}
        dados = json.dumps(resposta).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)
        print(f"[json-rpc] {pedido['method']}{tuple(pedido.get('params', []))} -> {resposta.get('result', resposta.get('error'))}")

    def log_message(self, *args) -> None:
        pass


print("JSON-RPC na porta 9801")
HTTPServer(("0.0.0.0", 9801), JsonRpc).serve_forever()
