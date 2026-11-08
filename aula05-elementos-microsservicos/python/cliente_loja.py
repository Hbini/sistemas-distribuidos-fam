"""
Aula 05: Cliente que usa SOMENTE o API Gateway.
Executar depois de subir os 4 serviços (ou o docker compose):
    python cliente_loja.py
"""
import json
import urllib.request

GATEWAY = "http://localhost:8000"


def chamar(metodo, caminho, corpo=None):
    dados = json.dumps(corpo).encode() if corpo else None
    req = urllib.request.Request(GATEWAY + caminho, data=dados, method=metodo,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


print("Cardápio:", chamar("GET", "/api/catalogo/produtos")[1])
print("Estoque da coxinha:", chamar("GET", "/api/estoque/estoque/1")[1])
print("Pedido 1:", chamar("POST", "/api/pedidos", {"produto_id": 1, "quantidade": 3}))
print("Pedido 2:", chamar("POST", "/api/pedidos", {"produto_id": 1, "quantidade": 50}))
print("Todos os pedidos:", chamar("GET", "/api/pedidos")[1])
