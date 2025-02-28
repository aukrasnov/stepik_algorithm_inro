import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    for i in range(5):
        time.sleep(1)
        print('.', end='', flush=True)
    print(' [x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_consume(queue='hello',
                      auto_ack=False,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

