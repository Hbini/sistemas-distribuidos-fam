# Exercícios: Aula 14

**Exercício 1 (cache e escrita concorrente).** Abra dois clientes do SAD. No cliente A, leia `notas.txt`; no cliente B, altere o arquivo; volte ao A e leia de novo. O A viu a alteração? Explique por quê. Agora imagine que o cliente pule a consulta de versão por 30 s para economizar rede (como o NFS faz): que problema de consistência aparece?

**Exercício 2 (conflito de escrita).** Dois clientes leem `notas.txt` v3 e ambos gravam uma alteração. A segunda gravação apaga a primeira ("lost update"). Implemente **controle otimista de concorrência**: a operação `escrever` passa a enviar a versão que o cliente leu, e o servidor recusa se a versão atual for diferente.

**Exercício 3 (balanceamento).** No `balanceador_carga.py`, a política "menor carga" supõe que o balanceador sabe exatamente quando cada servidor ficará livre. Implemente a política "dois aleatórios" (sorteia 2 servidores e escolhe o menos carregado entre eles) e compare o makespan. Por que ela é muito usada na prática?

**Exercício 4 (segurança).** Usando `integridade_hmac.py`, explique por que o HMAC sozinho não impede um **ataque de repetição** (o atacante reenvia a mesma mensagem válida 10 vezes). Proponha e implemente uma correção.
