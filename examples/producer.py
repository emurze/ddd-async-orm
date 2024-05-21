import sys

import pika

from containers import rabbit_container


def main(params) -> None:
    if len(params) == 0:
        raise ValueError("Params must be typed.")

    with rabbit_container.connection() as conn:
        channel = conn.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        channel.basic_publish(
            exchange="logs",
            routing_key="",
            body=params[0].encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )


if __name__ == '__main__':
    main(sys.argv[1:])
