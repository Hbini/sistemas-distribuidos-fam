# Aula 07: Paradigmas de comunicação em Sistemas Distribuídos

## Paradigmas demonstrados

| Paradigma | Ideia | Exemplo |
|---|---|---|
| Memória compartilhada | processos leem e escrevem a mesma memória; exige travas | `memoria_compartilhada.py`, `MemoriaCompartilhada.java` |
| Troca de mensagens | processos isolados que só conversam por mensagens | todos os exemplos com sockets |
| Publish/Subscribe | mensagem publicada em um tópico chega a **todos** os assinantes | `broker_pubsub.py` + `cliente_pubsub.py` / `ClientePubSub.java` |
| Fila de mensagens | cada mensagem vai para **um único** consumidor; fica guardada até ser consumida | `fila_mensagens.py` |

(Cliente/servidor e P2P ganham exemplos próprios nas Aulas 08 e 09.)

```
PUB/SUB                                  FILA (ponto a ponto)
                 +--> assinante 1         produtor --> [ m3 m2 m1 ] --> consumidor A (m1, m3)
publicador -->[broker]--> assinante 2                                 \-> consumidor B (m2)
                 +--> assinante 3
todos recebem a mesma mensagem           cada mensagem é processada uma única vez
```

## Como executar

```bash
python python/memoria_compartilhada.py
java   java/MemoriaCompartilhada.java

# Pub/Sub (vários terminais)
python python/broker_pubsub.py
python python/cliente_pubsub.py sub cardapio
java   java/ClientePubSub.java sub cardapio
python python/cliente_pubsub.py pub cardapio "Hoje tem feijoada"

# Fila de mensagens
python python/fila_mensagens.py broker
python python/fila_mensagens.py consumidor cozinha Chef-A
python python/fila_mensagens.py consumidor cozinha Chef-B
python python/fila_mensagens.py produtor cozinha 10
```

Experimente: na fila, inicie o produtor **antes** dos consumidores. Os pedidos esperam no broker (persistência). No pub/sub, publique sem nenhum assinante: a mensagem se perde (transiente).

Exercícios: [exercicios.md](exercicios.md)
