# Exercícios: Aula 12

**Exercício 1 (Lamport no papel e no código).** Crie um novo roteiro com 3 processos e pelo menos 4 mensagens. Calcule à mão os relógios de Lamport de todos os eventos, depois altere `relogio_lamport.py` (ou a versão Java) para executar o seu roteiro e confira.

**Exercício 2 (vetorial).** No roteiro do exercício 1, use relógios vetoriais e liste **todos** os pares de eventos concorrentes. Por que o relógio de Lamport sozinho não permite essa análise?

**Exercício 3 (eleição).** Rode `eleicao_bully.py` com 8 processos em três cenários: (a) P8 caiu e P7 detecta; (b) P8 caiu e P1 detecta; (c) P8 e P7 caíram e P1 detecta. Anote o número de mensagens de cada cenário e explique a diferença. Faça a mesma comparação com o algoritmo do anel.

**Exercício 4 (exclusão mútua centralizada).** Implemente a versão **centralizada** da exclusão mútua: um coordenador recebe `PEDIR`, responde `CONCEDIDO` (ou coloca na fila) e recebe `LIBERAR`. Compare com Ricart e Agrawala em número de mensagens e tolerância a falhas.
