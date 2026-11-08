"""
Aula 11: cliente RPC. Repare que NÃO há nenhum socket, send ou recv aqui:
o objeto 'servidor' é um PROXY (stub) gerado pelo middleware.
"""
import xmlrpc.client

servidor = xmlrpc.client.ServerProxy("http://127.0.0.1:9800")

print("Funções disponíveis:", servidor.system.listMethods())
print("somar(2, 3) =", servidor.somar(2, 3))                 # parece local, mas roda no servidor
print("Cardápio:", servidor.listar_cardapio())
print("Total de 2 coxinhas e 1 suco: R$", servidor.calcular_total({"coxinha": 2, "suco": 1}))

try:
    servidor.calcular_total({"pizza": 1})
except xmlrpc.client.Fault as erro:
    # Exceções do servidor também viajam pela rede e chegam aqui como Fault
    print("Erro remoto tratado no cliente:", erro.faultString)
