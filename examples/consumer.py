import contextlib
import time

from containers import rabbit_container


def callback(ch, method, properties, body) -> None:
    print(f"RECEIVED {body=}")
    time.sleep(body.count(b"."))
    print(f"DONE")


def main() -> None:
    with rabbit_container.connection() as conn:
        channel = conn.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = channel.queue_declare(queue='', durable=True, exclusive=True)
        channel.queue_bind(exchange='logs', queue=result.method.queue)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue="task_queue",
            on_message_callback=callback,
            auto_ack=True,
        )
        channel.start_consuming()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        main()
