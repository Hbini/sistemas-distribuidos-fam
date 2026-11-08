# Aula 02: Sistemas centralizados, distribuídos, paralelos e de alto desempenho

## O que estes exemplos mostram

| Modelo | Onde roda | Como as partes se comunicam | Exemplo nesta pasta |
|---|---|---|---|
| Centralizado / sequencial | 1 máquina, 1 fluxo de execução | não há partes | modo SEQUENCIAL de `sequencial_vs_paralelo` |
| Paralelo | 1 máquina, vários núcleos | memória da própria máquina | modo PARALELO de `sequencial_vs_paralelo` |
| Distribuído | várias máquinas | mensagens pela rede (TCP) | `coordenador_trabalhadores` |

Também calculamos duas métricas clássicas de alto desempenho (HPC):

* **Speedup** = tempo sequencial / tempo paralelo
* **Eficiência** = speedup / número de processadores

## Como executar

### Python (3.10 ou superior)

```bash
cd python
python sequencial_vs_paralelo.py
python sequencial_vs_paralelo.py 2     # testa com 2 processos

# distribuído: abra 3 terminais
python coordenador_trabalhadores.py trabalhador 6001
python coordenador_trabalhadores.py trabalhador 6002
python coordenador_trabalhadores.py coordenador 127.0.0.1:6001 127.0.0.1:6002
```

### Java (JDK 17 ou superior; recomendado JDK 21)

```bash
cd java
java SequencialVsParalelo.java

java CoordenadorTrabalhadores.java trabalhador 6001
java CoordenadorTrabalhadores.java trabalhador 6002
java CoordenadorTrabalhadores.java coordenador 127.0.0.1:6001 127.0.0.1:6002
```

## Experimento sugerido em sala

1. Rode o exemplo paralelo com 1, 2, 4 e 8 processos e anote os tempos.
2. Rode o exemplo distribuído com trabalhadores em computadores diferentes do laboratório.
3. Compare: por que o trabalhador que recebe o fim do intervalo demora mais? (Dica: números grandes custam mais para testar.)

Exercícios: [exercicios.md](exercicios.md)
