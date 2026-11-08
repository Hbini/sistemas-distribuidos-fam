"""
Aula 14: cliente do SAD com CACHE e validação por versão.
Executar (com o servidor rodando): python cliente_arquivos_cache.py
Abra dois clientes ao mesmo tempo, escreva em um e leia no outro.
"""
import json
import socket

sock = socket.create_connection(("127.0.0.1", 9950))
entrada = sock.makefile("r", encoding="utf-8")
cache: dict[str, dict] = {}
bytes_economizados = 0


def chamar(**pedido) -> dict:
    sock.sendall((json.dumps(pedido, ensure_ascii=False) + "\n").encode("utf-8"))
    return json.loads(entrada.readline())


def ler(nome: str) -> str:
    global bytes_economizados
    v = chamar(op="versao", nome=nome)
    if not v["ok"]:
        return "(arquivo não existe)"
    if nome in cache and cache[nome]["versao"] == v["versao"]:
        bytes_economizados += len(cache[nome]["conteudo"].encode())
        return f"{cache[nome]['conteudo']}   [CACHE válido, v{v['versao']}]"
    dados = chamar(op="ler", nome=nome)
    cache[nome] = {"conteudo": dados["conteudo"], "versao": dados["versao"]}
    return f"{dados['conteudo']}   [baixado do servidor, v{dados['versao']}]"


def escrever(nome: str, conteudo: str) -> None:
    r = chamar(op="escrever", nome=nome, conteudo=conteudo)
    cache[nome] = {"conteudo": conteudo, "versao": r["versao"]}
    print(f"gravado {nome} v{r['versao']}")


print("Comandos: ls | cat <arquivo> | echo <arquivo> <texto> | sair")
while True:
    partes = input("SAD> ").split(" ", 2)
    if partes[0] == "ls":
        print(chamar(op="listar")["arquivos"])
    elif partes[0] == "cat" and len(partes) > 1:
        print(ler(partes[1]))
    elif partes[0] == "echo" and len(partes) > 2:
        escrever(partes[1], partes[2])
    elif partes[0] == "sair":
        break
print(f"Bytes que deixaram de trafegar graças ao cache: {bytes_economizados}")
