# Exercícios: Aula 11

**Exercício 1 (RPC).** Acrescente ao servidor XML-RPC a função `fazer_pedido(cliente, itens)` que guarda o pedido em uma lista e devolve o número do pedido, e a função `listar_pedidos()`. Chame-as a partir de dois clientes ao mesmo tempo. O servidor `SimpleXMLRPCServer` atende requisições em paralelo? Como você verificaria?

**Exercício 2 (RMI com callback).** No RMI, o cliente também pode exportar um objeto remoto. Crie a interface `Notificador` com o método `pedidoPronto(String msg)`, faça o cliente registrar-se no servidor e faça o servidor avisar o cliente 3 segundos após `fazerPedido`. Que paradigma de comunicação você implementou?

**Exercício 3 (MOM).** Com o RabbitMQ rodando, envie 10 pedidos **sem nenhum consumidor ativo**, reinicie o container do RabbitMQ (`docker compose restart`) e só então ligue o consumidor. Os pedidos sobreviveram? Repita retirando `durable=True` e `delivery_mode` do produtor. Explique a diferença.

**Exercício 4 (conceitual).** Compare RPC, RMI, REST e MOM quanto a: acoplamento temporal, acoplamento de linguagem, modelo síncrono ou assíncrono e um caso de uso adequado para cada um.
