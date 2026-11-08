# Exercícios: Aula 07

**Exercício 1 (tópicos hierárquicos).** Altere o broker pub/sub para aceitar o curinga `*` no final do tópico: quem assina `cardapio.*` deve receber mensagens de `cardapio.almoco` e `cardapio.jantar`.

**Exercício 2 (confirmação de processamento).** Na fila de mensagens, se o consumidor travar depois do `GET`, o pedido some. Implemente confirmação (ACK): o `GET` move a mensagem para uma lista "em processamento"; o consumidor envia `ACK <id>` ao terminar; se o ACK não chegar em 5 segundos, a mensagem volta para a fila. Que garantia de entrega você obteve: at-most-once, at-least-once ou exactly-once?

**Exercício 3 (consumidor Java).** Escreva `ConsumidorFila.java`, compatível com `fila_mensagens.py`, e coloque um consumidor Java e um Python atendendo a mesma fila ao mesmo tempo.

**Exercício 4 (conceitual).** Para cada cenário, escolha entre memória compartilhada, cliente/servidor, pub/sub ou fila, justificando: (a) notificar todos os celulares de alunos quando sai uma nota; (b) distribuir 10.000 e-mails para 5 servidores de envio; (c) consultar o saldo bancário; (d) várias threads de um jogo atualizando o placar na mesma máquina.
