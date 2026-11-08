"""
Aula 11: Middleware de comunicação: RPC (Remote Procedure Call) com XML-RPC.

Compare com a Aula 08: lá nós montávamos as mensagens na mão (sockets,
protocolo de texto, delimitadores). Aqui o MIDDLEWARE faz tudo isso:
  * marshalling dos parâmetros (vira XML)
  * transporte (HTTP sobre TCP)
  * despacho para a função certa no servidor
  * unmarshalling do resultado

Para o programador, chamar uma função remota fica igual a chamar uma local.
Isso é TRANSPARÊNCIA DE ACESSO oferecida pelo middleware.

Executar: python rpc_servidor.py      e depois   python rpc_cliente.py
"""

from xmlrpc.server import SimpleXMLRPCServer

cardapio = {"coxinha": 7.5, "pastel": 9.0, "suco": 6.0}


def listar_cardapio() -> dict:
    return cardapio


def calcular_total(itens: dict) -> float:
    """itens = {"coxinha": 2, "suco": 1}"""
    return sum(cardapio[nome] * qtd for nome, qtd in itens.items())


def somar(a, b):
    return a + b


servidor = SimpleXMLRPCServer(("0.0.0.0", 9800), allow_none=True, logRequests=True)
servidor.register_introspection_functions()          # permite o cliente perguntar "quais funções existem?"
servidor.register_function(listar_cardapio)
servidor.register_function(calcular_total)
servidor.register_function(somar)
print("Servidor RPC na porta 9800. Funções: listar_cardapio, calcular_total, somar")
servidor.serve_forever()
