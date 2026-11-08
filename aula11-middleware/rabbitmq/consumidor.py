"""
Aula 11: consumidor RabbitMQ com confirmação manual (ACK).
Abra 2 ou 3 consumidores e veja o RabbitMQ distribuir os pedidos entre eles.
Executar: python consumidor.py Chef-A
"""
import sys
import time

import pika

nome = sys.argv[1] if len(sys.argv) > 1 else "consumidor"
conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
canal = conexao.channel()
canal.queue_declare(queue="pedidos", durable=True)
canal.basic_qos(prefetch_count=1)          # entrega 1 mensagem por vez a cada consumidor


def processar(ch, metodo, propriedades, corpo):
    print(f"[{nome}] preparando {corpo.decode()}...")
    time.sleep(1)
    ch.basic_ack(delivery_tag=metodo.delivery_tag)   # só agora a mensagem sai da fila


canal.basic_consume(queue="pedidos", on_message_callback=processar)
print(f"[{nome}] aguardando pedidos. Ctrl+C para sair.")
canal.start_consuming()
