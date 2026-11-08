# Aula 11: Middleware

## Onde fica o middleware

```
   +-------------------------------------------+
   |        Aplicação distribuída               |   lanchonete, banco, loja...
   +-------------------------------------------+
   |   MIDDLEWARE  (RPC, RMI, MOM, REST...)     |   marshalling, nomes, transporte,
   |                                            |   tratamento de erros, filas
   +-------------------------------------------+
   |   Sistema operacional + rede (sockets)     |   o que usamos "na mão" na Aula 08
   +-------------------------------------------+
```

## Tipos de middleware demonstrados

| Tipo | Abstração | Exemplo |
|---|---|---|
| RPC | chamar uma **função** remota | `rpc_servidor.py` / `rpc_cliente.py` (XML-RPC) |
| RPC entre linguagens | contrato padronizado (JSON-RPC 2.0) | `jsonrpc_servidor.py` (Python) + `ClienteJsonRpc.java` |
| Objetos distribuídos (RMI) | chamar um **método** de um objeto remoto | `ServidorRMI.java` / `ClienteRMI.java` |
| MOM (orientado a mensagens) | filas persistentes com ACK | pasta `rabbitmq/` (requer Docker) |

## Como executar

```bash
# RPC
python python/rpc_servidor.py
python python/rpc_cliente.py

# Interoperabilidade Python <-> Java
python python/jsonrpc_servidor.py
java   java/ClienteJsonRpc.java

# Java RMI
java java/ServidorRMI.java
java java/ClienteRMI.java

# RabbitMQ (MOM)
cd rabbitmq
docker compose up -d
pip install -r requirements.txt
python consumidor.py Chef-A        # abra 2 consumidores
python consumidor.py Chef-B
python produtor.py 10
# painel: http://localhost:15672  (guest / guest)
```

## Para observar

* No `rpc_cliente.py` e no `ClienteRMI.java` **não existe nenhum socket**. O middleware gerou um *stub* (proxy).
* No RMI, imprima `lanchonete.getClass()`: o objeto é um `$Proxy`, não a classe real.
* No RabbitMQ, pare um consumidor no meio do processamento (Ctrl+C): a mensagem sem ACK volta para a fila e outro consumidor a recebe.

Exercícios: [exercicios.md](exercicios.md)
