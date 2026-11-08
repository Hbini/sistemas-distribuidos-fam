# Exercícios: Aula 03

**Exercício 1 (flexibilidade).** Acrescente as operações `POT` (potência) e `MOD` (resto da divisão) à réplica Python **e** à réplica Java. Quantas linhas você precisou alterar? O cliente precisou mudar? Relacione com o conceito de sistema aberto.

**Exercício 2 (confiabilidade).** Hoje uma réplica que caiu continua registrada para sempre. Implemente no serviço de nomes um mecanismo de **heartbeat**: cada réplica envia `VIVO calculadora <host> <porta>` a cada 2 segundos e o serviço de nomes remove da lista quem ficar mais de 6 segundos sem enviar.

**Exercício 3 (medição de disponibilidade).** Rode o cliente por 60 segundos com 3 réplicas e derrube uma réplica a cada 15 segundos. Calcule a disponibilidade observada (pedidos atendidos / pedidos feitos). Depois responda: qual seria a disponibilidade teórica do serviço se cada réplica tivesse disponibilidade de 95% e as falhas fossem independentes? (Fórmula: 1 menos (1 menos 0,95) elevado ao número de réplicas.)

**Exercício 4 (conceitual).** Para cada tipo de transparência (acesso, localização, migração, relocação, replicação, concorrência e falha), dê um exemplo de um sistema que você usa no dia a dia e diga se ele oferece ou não aquela transparência.
