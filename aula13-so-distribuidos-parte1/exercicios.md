# Exercícios: Aula 13

**Exercício 1 (detector adaptativo).** Faça o nó de heartbeat ficar "lento" de propósito (atraso aleatório entre 0,5 e 4 s). Observe falsos positivos de SUSPEITO. Proponha e implemente um ajuste no monitor que reduza os falsos positivos. Qual o custo da sua solução?

**Exercício 2 (quórum).** Modifique a escrita forte para exigir confirmação de apenas uma **maioria** (2 de 3 réplicas) e a leitura para consultar 2 réplicas e devolver o valor mais novo (use um número de versão). Mostre que, com R3 isolada, o sistema continua aceitando escritas e leituras corretas. Relacione com a regra W + R > N.

**Exercício 3 (frequência de checkpoint).** No `checkpoint_rollback.py`, compare checkpoints a cada 10, 100 e 500 lotes quanto a: trabalho perdido na falha e quantidade de gravações em disco. Qual intervalo você escolheria e por quê?

**Exercício 4 (CAP).** Classifique como CP ou AP e justifique: (a) transferência PIX; (b) contador de curtidas do Instagram; (c) reserva do último assento de um voo; (d) carrinho de compras da Amazon; (e) DNS.
