# Exercícios: Aula 04

**Exercício 1 (curva de escalabilidade).** Para o modelo `pool` com 4 threads, rode o gerador com 1, 5, 10, 20, 50 e 100 clientes simultâneos. Faça um gráfico (planilha) de vazão e latência média em função do número de clientes. Identifique o ponto de saturação e explique o que acontece com a latência depois dele.

**Exercício 2 (gargalo de CPU).** Troque o `time.sleep(TEMPO_SERVICO)` do servidor Python por um cálculo pesado (por exemplo, somar os quadrados de 0 a 2.000.000). Repita a comparação entre `pool` e `thread`. O modo `thread` continua ganhando? Explique o resultado usando o conceito de GIL do Python e compare com a versão Java.

**Exercício 3 (Amdahl).** Um sistema de relatórios leva 100 s, dos quais 20 s são leitura sequencial do banco de dados e 80 s são processamento paralelizável. (a) Qual o speedup com 4, 16 e infinitos processadores? (b) Vale a pena comprar um servidor com 64 núcleos em vez de 16? Justifique com números.

**Exercício 4 (proteção contra sobrecarga).** Modifique o servidor no modo `pool` para recusar imediatamente (responder `OCUPADO`) quando já houver mais de 20 pedidos esperando na fila. Meça a latência dos pedidos aceitos com 100 clientes simultâneos e compare com a versão sem limite. Qual é o nome desta técnica?
