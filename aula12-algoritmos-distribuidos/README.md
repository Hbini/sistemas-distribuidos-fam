# Aula 12: Algoritmos distribuídos

"Distribuir é fácil, coordenar é o desafio." Os exemplos são **simulações didáticas**: rodam em uma só máquina e mostram, mensagem por mensagem, o que cada algoritmo faz, para você conferir no quadro.

| Problema clássico | Algoritmo | Python | Java |
|---|---|---|---|
| Ordem de eventos sem relógio global | Relógio lógico de Lamport | `relogio_lamport.py` | `RelogioLamport.java` |
| Causalidade e concorrência | Relógio vetorial | `relogio_vetorial.py` | `RelogioVetorial.java` |
| Eleição de líder | Valentão (Bully) | `eleicao_bully.py` | `EleicaoBully.java` |
| Eleição de líder | Anel (Chang e Roberts) | `eleicao_anel.py` | |
| Exclusão mútua distribuída | Ricart e Agrawala | `exclusao_mutua_ricart_agrawala.py` | `RicartAgrawala.java` |
| Sincronização de relógios físicos | Berkeley | `sincronizacao_berkeley.py` | |

## Como executar

```bash
python python/relogio_lamport.py
python python/relogio_vetorial.py
python python/eleicao_bully.py               # 5 processos, P5 caiu, P2 detecta
python python/eleicao_bully.py 7 3 7 6       # 7 processos, P3 detecta, caíram P7 e P6
python python/eleicao_anel.py
python python/exclusao_mutua_ricart_agrawala.py
python python/sincronizacao_berkeley.py

java java/RelogioLamport.java
java java/RelogioVetorial.java
java java/EleicaoBully.java 5 2 5
java java/RicartAgrawala.java
```

## Resumo comparativo

| Algoritmo | Mensagens | Ponto fraco |
|---|---|---|
| Bully | O(n²) no pior caso | muito tráfego quando o menor id detecta a falha |
| Anel | 2n | lento: a mensagem precisa dar a volta completa |
| Ricart e Agrawala | 2(n menos 1) por entrada | a falha de QUALQUER processo trava todos (ninguém responde OK) |
| Exclusão centralizada | 3 por entrada | coordenador é ponto único de falha |

Para consenso tolerante a falhas na prática (etcd, Kubernetes, Consul), veja a visualização interativa do **Raft** em https://raft.github.io

Exercícios: [exercicios.md](exercicios.md)
