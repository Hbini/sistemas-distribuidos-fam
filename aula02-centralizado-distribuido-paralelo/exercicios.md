# Exercícios: Aula 02

**Exercício 1 (medição).** Execute `sequencial_vs_paralelo` com 1, 2, 4 e 8 processos (ou threads, no Java). Monte uma tabela com tempo, speedup e eficiência. A partir de quantos processos o ganho deixa de valer a pena na sua máquina? Explique por quê.

**Exercício 2 (balanceamento de carga).** No exemplo distribuído, o último trabalhador sempre demora mais. Altere o coordenador para dividir o trabalho em **muitos pedaços pequenos** (por exemplo, 20) e entregar um novo pedaço a cada trabalhador assim que ele terminar o anterior. Compare o tempo total antes e depois.

**Exercício 3 (heterogeneidade).** O coordenador Python fala JSON e o trabalhador Java fala texto `inicio;fim`. Modifique o trabalhador **Java** para entender o mesmo protocolo JSON do Python (uma linha `{"inicio": 0, "fim": 1000}` e resposta `{"primos": 168, "tempo": 0.01, "host": "pc01"}`), de modo que o coordenador Python consiga usar trabalhadores Java.

**Exercício 4 (conceitual).** Classifique cada sistema como centralizado, paralelo, distribuído ou HPC e justifique: (a) caixa eletrônico de um banco; (b) renderização de um filme em uma placa de vídeo; (c) o Google Drive; (d) um supercomputador simulando o clima; (e) uma planilha Excel em um notebook.
