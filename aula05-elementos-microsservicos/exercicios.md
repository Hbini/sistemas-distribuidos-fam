# Exercícios: Aula 05

**Exercício 1 (novo microsserviço).** Crie um microsserviço `pagamentos` (porta 8004, linguagem à sua escolha) com a rota `POST /pagamentos` que recebe `{"pedido": 1, "valor": 22.5}` e aprova pagamentos de até R$ 100,00 (acima disso, responde 402). Faça o serviço de pedidos chamá-lo antes de confirmar o pedido e registre-o no gateway e no `docker-compose.yml`.

**Exercício 2 (consistência entre serviços).** No exercício 1, o que acontece com o estoque se o pagamento for recusado **depois** da baixa? Implemente uma **ação de compensação**: se o pagamento falhar, o serviço de pedidos chama `POST /estoque/{id}/devolver` (crie esta rota no serviço Java). Pesquise e explique o padrão **Saga**.

**Exercício 3 (resiliência).** Faça o serviço de pedidos tentar novamente (retry) até 3 vezes, com espera de 0,5 s, 1 s e 2 s, quando o estoque responder 503. Qual o nome desta estratégia de espera? Por que não é bom repetir indefinidamente?

**Exercício 4 (conceitual).** Compare monólito e microsserviços em: implantação, escalabilidade, isolamento de falhas, consistência de dados e complexidade operacional. Em qual situação você recomendaria um monólito para a lanchonete da faculdade?
