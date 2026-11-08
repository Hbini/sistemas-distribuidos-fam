# Aula 13: Sistemas Operacionais Distribuídos (Parte 1): tolerância a falhas, replicação e CAP

| Conceito | Python | Java |
|---|---|---|
| Detecção de falhas (heartbeat + timeout) | `detector_falhas_heartbeat.py` | `NoHeartbeat.java` (nó compatível) |
| Consistência forte x eventual e teorema CAP | `consistencia_forte_eventual.py` | `ConsistenciaReplicas.java` |
| Recuperação: checkpoint e rollback | `checkpoint_rollback.py` | |

## Teorema CAP em uma figura

```
            Consistência (C)
                 /\
                /  \        Com partição de rede (P), escolha:
               /    \         CP: recusa a operação para não divergir (bancos, estoque)
              /      \        AP: responde, mesmo com dado antigo (redes sociais, DNS, carrinho)
   Disponib. (A) ---- Tolerância a partição (P)
```

## Como executar

```bash
python python/detector_falhas_heartbeat.py monitor
python python/detector_falhas_heartbeat.py no servidor-A
java   java/NoHeartbeat.java servidor-Java
# feche um nó (Ctrl+C) e observe OK -> SUSPEITO -> FALHO

python python/consistencia_forte_eventual.py
java   java/ConsistenciaReplicas.java

python python/checkpoint_rollback.py      # cai no lote 437
python python/checkpoint_rollback.py      # retoma do lote 400
```

Exercícios: [exercicios.md](exercicios.md)
