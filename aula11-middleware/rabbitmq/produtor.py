"""
Aula 11: produtor de mensagens no RabbitMQ (MOM real).
Pré-requisitos: docker compose up -d   e   pip install -r requirements.txt

Compare com fila_mensagens.py (Aula 07): o conceito é o mesmo, mas agora
o broker é um middleware profissional, com persistência em disco, ACK,
painel de monitoramento e clientes para dezenas de linguagens.

Executar: python produtor.py 10
"""
import sys

import pika

conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
canal = conexao.channel()
canal.queue_declare(queue="pedidos", durable=True)        # durable: a fila sobrevive a reinício

for i in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 6):
    canal.basic_publish(
        exchange="",
        routing_key="pedidos",
        body=f"pedido-{i}".encode(),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),  # grava em disco
    )
    print(f"enviado pedido-{i}")
conexao.close()
