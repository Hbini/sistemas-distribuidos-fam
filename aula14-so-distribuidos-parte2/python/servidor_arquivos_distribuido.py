"""
Aula 14: Sistema de arquivos distribuído (SAD) simplificado, no estilo NFS.

O servidor guarda os arquivos e um NÚMERO DE VERSÃO para cada um.
O cliente (cliente_arquivos_cache.py) mantém um CACHE local:
  * leitura: pergunta só a VERSÃO (mensagem pequena); se for igual à do cache,
    usa a cópia local, sem baixar o conteúdo de novo (transparência + desempenho);
  * escrita: envia ao servidor, que incrementa a versão (write-through).

Protocolo (JSON por linha): {"op": "versao"|"ler"|"escrever"|"listar", "nome": ..., "conteudo": ...}
Executar: python servidor_arquivos_distribuido.py
"""
import json
import socket
import threading

arquivos: dict[str, dict] = {"leiame.txt": {"conteudo": "Bem-vindo ao SAD da FAM!", "versao": 1}}
trava = threading.Lock()


def tratar(pedido: dict) -> dict:
    nome = pedido.get("nome", "")
    with trava:
        if pedido["op"] == "listar":
            return {"ok": True, "arquivos": {n: a["versao"] for n, a in arquivos.items()}}
        if pedido["op"] == "versao":
            return {"ok": nome in arquivos, "versao": arquivos.get(nome, {}).get("versao")}
        if pedido["op"] == "ler":
            if nome not in arquivos:
                return {"ok": False, "erro": "arquivo não existe"}
            return {"ok": True, **arquivos[nome]}
        if pedido["op"] == "escrever":
            atual = arquivos.get(nome, {"versao": 0})
            arquivos[nome] = {"conteudo": pedido["conteudo"], "versao": atual["versao"] + 1}
            return {"ok": True, "versao": arquivos[nome]["versao"]}
    return {"ok": False, "erro": "operação inválida"}


def atender(c: socket.socket) -> None:
    with c, c.makefile("r", encoding="utf-8") as f:
        for linha in f:
            pedido = json.loads(linha)
            resposta = tratar(pedido)
            print(f"[SAD] {pedido['op']:<9} {pedido.get('nome', ''):<12} -> {resposta.get('versao', '')}")
            c.sendall((json.dumps(resposta, ensure_ascii=False) + "\n").encode("utf-8"))


srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 9950))
srv.listen()
print("[SAD] servidor de arquivos na porta 9950")
while True:
    conexao, _ = srv.accept()
    threading.Thread(target=atender, args=(conexao,), daemon=True).start()
