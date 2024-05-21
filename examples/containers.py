import pika
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from pika.adapters.blocking_connection import BlockingChannel


def get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(username='adm1', password='adm1')
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=credentials,
    )
    return pika.BlockingConnection(parameters=parameters)


def get_channel(connection: pika.BlockingConnection) -> BlockingChannel:
    return connection.channel()


class RabbitMQContainer(DeclarativeContainer):
    connection = Singleton(get_connection)
    channel = Singleton(get_channel, connection)


rabbit_container = RabbitMQContainer()
