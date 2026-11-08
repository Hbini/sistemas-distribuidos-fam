# Aula 08: Mecanismos de comunicação entre processos: Paradigma cliente/servidor e Sockets

## Ciclo de vida de um socket TCP

```
        SERVIDOR                                CLIENTE
   socket()                                socket()
   bind(ip, porta)                              |
   listen()                                     |
   accept()  <-------- conexão (3-way handshake) ------ connect(ip, porta)
      |                                         |
   recv()   <------------- dados -------------- send()
   send()   -------------- dados -------------> recv()
   close()                                 close()
```

## Arquivos

| Exemplo | Python | Java | Porta |
|---|---|---|---|
| Eco iterativo (um cliente por vez) | `eco_servidor.py`, `eco_cliente.py` | `EcoServidor.java`, `EcoCliente.java` | 9500 |
| Servidor concorrente (thread por cliente) | `servidor_multicliente.py` | (ver Aula 04, `ServidorModelos.java`) | 9500 |
| Chat em grupo | `chat_servidor.py`, `chat_cliente.py` | `ChatServidor.java`, `ChatCliente.java` | 9600 |

Clientes e servidores Python e Java são **intercambiáveis**: um cliente Java conversa com um servidor Python e vice-versa.

## Como executar

```bash
python python/eco_servidor.py            # ou java java/EcoServidor.java
python python/eco_cliente.py             # ou java java/EcoCliente.java

python python/chat_servidor.py           # ou java java/ChatServidor.java
python python/chat_cliente.py ana
java   java/ChatCliente.java bruno
```

### No laboratório (máquinas diferentes)

1. No servidor, descubra o IP: `ipconfig` (Windows) ou `ip a` (Linux).
2. Libere a porta no firewall, se necessário.
3. No cliente: `python chat_cliente.py ana 192.168.0.15`.

## Experimento: o problema do servidor iterativo

Com `eco_servidor.py` rodando, abra **dois** `eco_cliente.py`. O segundo não recebe resposta até o primeiro sair. Repita com `servidor_multicliente.py`.

## Armadilha importante: TCP é um FLUXO de bytes

`recv(1024)` não devolve "uma mensagem": devolve os bytes que chegaram até agora. Duas mensagens podem chegar juntas ou uma pode chegar em pedaços. Por isso os exemplos do chat usam **uma linha por mensagem** (delimitador `\n`). Isso é chamado de **enquadramento (framing)** e é tema do Exercício 2.

Exercícios: [exercicios.md](exercicios.md)
