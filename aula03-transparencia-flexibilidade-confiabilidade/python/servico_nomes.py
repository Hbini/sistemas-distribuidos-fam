"""
Aula 03: Propriedades críticas: TRANSPARÊNCIA DE LOCALIZAÇÃO.

Serviço de nomes (uma "lista telefônica" do sistema distribuído).
Os servidores se REGISTRAM com um nome lógico ("calculadora") e os clientes
perguntam "onde está a calculadora?" sem saber IP nem porta de antemão.
É a mesma ideia do DNS, do Consul, do Eureka e do service discovery do Kubernetes.

Protocolo de TEXTO, uma linha por mensagem (igual nas versões Python e Java):
    REGISTRAR <nome> <host> <porta>   ->  OK
    RESOLVER  <nome>                  ->  host:porta,host:porta,...   (ou VAZIO)
    LISTAR                            ->  nome=host:porta;...

Como executar:
    python servico_nomes.py            (escuta na porta 5000)
"""

import socket
import threading

PORTA = 5000
registro: dict[str, list[str]] = {}   # nome lógico -> lista de endereços físicos
trava = threading.Lock()              # várias threads acessam o mesmo dicionário


def atender(conexao: socket.socket, endereco) -> None:
    with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
        for linha in entrada:
            partes = linha.split()
            if not partes:
                continue
            comando = partes[0].upper()
            if comando == "REGISTRAR" and len(partes) == 4:
                _, nome, host, porta = partes
                with trava:
                    lista = registro.setdefault(nome, [])
                    if f"{host}:{porta}" not in lista:
                        lista.append(f"{host}:{porta}")
                print(f"[nomes] {nome} registrado em {host}:{porta}")
                resposta = "OK"
            elif comando == "RESOLVER" and len(partes) == 2:
                with trava:
                    resposta = ",".join(registro.get(partes[1], [])) or "VAZIO"
            elif comando == "LISTAR":
                with trava:
                    resposta = ";".join(f"{n}={','.join(e)}" for n, e in registro.items()) or "VAZIO"
            else:
                resposta = "ERRO comando desconhecido"
            conexao.sendall((resposta + "\n").encode("utf-8"))


def main() -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", PORTA))
    servidor.listen()
    print(f"[nomes] serviço de nomes ouvindo na porta {PORTA}")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=atender, args=(conexao, endereco), daemon=True).start()


if __name__ == "__main__":
    main()
