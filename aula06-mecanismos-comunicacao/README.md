# Aula 06: Mecanismos de comunicação entre processos: elementos básicos

## Conceitos demonstrados

| Conceito | Arquivo Python | Arquivo Java |
|---|---|---|
| Serialização (JSON, binário, pickle) | `serializacao_marshalling.py` | `EndiannessDemo.java` |
| Marshalling binário entre linguagens | `servidor_binario.py` + `cliente_binario.py` | `ClienteBinario.java` (lê o servidor Python) |
| Endianness (ordem dos bytes) | `serializacao_marshalling.py` | `EndiannessDemo.java` |
| UDP sem garantia x TCP confiável | `udp_vs_tcp.py` | `UdpEco.java` (compatível com o Python) |
| Síncrona x assíncrona | `sincrona_vs_assincrona.py` | `SincronaAssincrona.java` |
| Transiente x persistente | `sincrona_vs_assincrona.py` (parte 3) | |

## Taxonomia da comunicação

```
                     |  TRANSIENTE (sem armazenamento)  |  PERSISTENTE (fica guardada)
---------------------+----------------------------------+------------------------------
SÍNCRONA (espera)    |  RPC, HTTP request/response      |  (raro) envio confirmado em fila
ASSÍNCRONA (segue)   |  UDP, notificação "fire & forget"|  e-mail, RabbitMQ, Kafka
```

## Como executar

```bash
python python/serializacao_marshalling.py
java   java/EndiannessDemo.java

python python/servidor_binario.py          # terminal 1
python python/cliente_binario.py           # terminal 2
java   java/ClienteBinario.java            # Java lendo bytes gerados pelo Python

python python/udp_vs_tcp.py servidor       # ou: java java/UdpEco.java servidor
python python/udp_vs_tcp.py cliente        # ou: java java/UdpEco.java cliente

python python/sincrona_vs_assincrona.py
java   java/SincronaAssincrona.java
```

Exercícios: [exercicios.md](exercicios.md)
