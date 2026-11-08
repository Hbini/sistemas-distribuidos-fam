# Aula 04: Propriedades críticas: Desempenho e Escalabilidade

## O que estes exemplos mostram

* **Vazão (throughput):** quantos pedidos por segundo o sistema atende.
* **Latência:** quanto tempo cada pedido leva, em média e no percentil 95 (p95).
* **Gargalo:** um servidor sequencial com 200 ms por pedido nunca passa de 5 pedidos/s, não importa quantos clientes cheguem.
* **Escalabilidade vertical x horizontal:** mais threads na mesma máquina (vertical) ou mais máquinas/réplicas (horizontal, Aula 03).
* **Lei de Amdahl e de Gustafson:** o limite teórico do ganho com paralelismo.

## Resultado de referência (10 clientes x 2 pedidos, 200 ms por pedido)

| Modelo | Vazão | Latência média |
|---|---|---|
| sequencial | 5 pedidos/s | 1.553 ms |
| pool de 4 threads | 20 pedidos/s | 421 ms |
| uma thread por cliente | 49 pedidos/s | 202 ms |

Os números variam de máquina para máquina, mas a proporção se mantém.

## Como executar

```bash
# Terminal 1: escolha UM modelo
python python/servidor_modelos.py sequencial 8000
python python/servidor_modelos.py pool 8000 4
python python/servidor_modelos.py thread 8000
java   java/ServidorModelos.java virtual 8000          # virtual threads (Java 21)

# Terminal 2: gere carga (servidores e geradores Python/Java são intercambiáveis)
python python/gerador_carga.py 127.0.0.1 8000 20 5
java   java/GeradorCarga.java 127.0.0.1 8000 20 5

# Lei de Amdahl
python python/amdahl.py
python python/amdahl.py 0.05
```

Exercícios: [exercicios.md](exercicios.md)
