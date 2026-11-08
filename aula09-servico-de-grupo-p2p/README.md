# Aula 09: Paradigmas de comunicação e sincronização: serviço de grupo, eventos e peer-to-peer

## Exemplos

| Conceito | Python | Java |
|---|---|---|
| Serviço de grupo com IP multicast | `multicast_grupo.py` | `MulticastMembro.java` (mesmo grupo) |
| Sincronização do grupo: ordem total com sequenciador | `ordem_total_sequenciador.py` | `OrdemTotal.java` |
| Peer-to-peer com busca por inundação e TTL | `no_p2p.py` | `NoP2P.java` (entra na mesma rede P2P) |

A comunicação por **eventos** (publish/subscribe) foi implementada na Aula 07 (`broker_pubsub.py`).

## Ordem total: por que importa

```
            SEM sequenciador                        COM sequenciador
 réplica 1: =100, +=10, *=2  -> 220        todas: (1) =100, (2) +=10, (3) *=2 -> 220
 réplica 2: +=10, =100, *=2  -> 200        mensagens adiantadas esperam na fila
 réplica 3: =100, *=2, +=10  -> 210        até chegar a vez do seu número
```

## Topologia da demonstração P2P

```
  A(8101) ---- B(8102) ---- C(8103)  [aula09.pdf, musica.mp3]
     |                         |
  D(8104) ------------------ E(8105) [aula09.pdf]
```

## Como executar

```bash
# Multicast (vários terminais ou várias máquinas na mesma rede local)
python python/multicast_grupo.py Ana
python python/multicast_grupo.py Bruno
java   java/MulticastMembro.java Carla

# Ordem total
python python/ordem_total_sequenciador.py
java   java/OrdemTotal.java

# P2P
python python/no_p2p.py demo
# rede mista Python + Java:
python python/no_p2p.py no 8201 --arquivos segredo.txt --vizinhos 127.0.0.1:8202
java   java/NoP2P.java 8202 - 127.0.0.1:8201          # depois digite: segredo.txt
```

Exercícios: [exercicios.md](exercicios.md)
