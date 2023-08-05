import amqpstorm

from injector import inject
from limecore.messaging.api import Message, Publisher as _Publisher

from .configuration import Configuration


class Publisher(_Publisher):
    @inject
    def __init__(self, configuration: Configuration):
        self._configuration = configuration

        self._channel = None
        self._connection = None

    def __enter__(self):
        self._connection = amqpstorm.Connection(
            self._configuration.host,
            self._configuration.user,
            self._configuration.password,
        ).__enter__()
        self._channel = self._connection.channel().__enter__()

        return self

    def __exit__(self, *args, **kwargs):
        self._channel.__exit__(*args, **kwargs)
        self._connection.__exit__(*args, **kwargs)

    def publish(self, msg: Message, mandatory: bool = True, queue: str = None):
        assert self._channel is not None

        if queue is not None:
            # If a named Queue is specified, declare it to ensure it exist.
            self._channel.queue.declare(queue, durable=True)
        else:
            # If no named Quue is specified, declare the default exchange which
            # will route the message.
            self._channel.exchange.declare(
                self._configuration.exchange, exchange_type="direct"
            )

        # Create the Message Properties
        properties = {
            "content_type": "application/json",
        }

        # Create the actual Message
        message = amqpstorm.Message.create(self._channel, msg.to_json(), properties)

        # Publish the Message to the Queue
        message.publish(
            exchange=queue is None and self._configuration.exchange or "",
            mandatory=mandatory,
            routing_key=queue is None and msg.routing_key or queue,
        )
