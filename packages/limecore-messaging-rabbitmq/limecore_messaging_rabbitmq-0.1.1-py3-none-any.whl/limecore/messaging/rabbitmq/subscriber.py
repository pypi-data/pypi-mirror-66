import amqpstorm

from functools import partial
from injector import Injector, inject
from limecore.messaging.api import (
    Handler,
    Message,
    RollbackException,
    RollbackStrategy,
    Subscriber as _Subscriber,
    Subscription,
)
from logging import Logger
from typing import Callable, List

from .configuration import Configuration


class Subscriber(_Subscriber):
    @inject
    def __init__(
        self,
        configuration: Configuration,
        get_logger: Callable[[str], Logger],
        injector: Injector,
    ):
        self._configuration = configuration
        self._injector = injector
        self._logger = get_logger(self.__class__.__name__)
        self._subscriptions: List[Subscription] = []

    def add_subscription(self, subscription: Subscription):
        self._subscriptions.append(subscription)

        return self

    def run(self):
        self._logger.info("Starting RabbitMQ Subscriber.")

        with amqpstorm.Connection(
            self._configuration.host,
            self._configuration.user,
            self._configuration.password,
        ) as connection:
            with connection.channel() as channel:
                self._logger.info(
                    "Declaring %s Exchange." % self._configuration.exchange
                )
                # Ensure the Exchange exists.
                channel.exchange.declare(
                    self._configuration.exchange, exchange_type="direct"
                )

                # Set QoS to limit number of messages that the consumer will prefetch
                # from the remote.
                channel.basic.qos(self._configuration.prefetch_count)

                # Set up the Subscriptions.
                for subscription in self._subscriptions:
                    self._logger.info("Declaring %s Queue." % subscription.queue)
                    # Ensure the Queue exists.
                    channel.queue.declare(subscription.queue, durable=True)

                    self._logger.info(
                        "Binding queue %s to %s, on %s."
                        % (
                            subscription.queue,
                            subscription.routing_key,
                            self._configuration.exchange,
                        )
                    )
                    # Bind the Queue to the Exchange for the Routing Key.
                    channel.queue.bind(
                        subscription.queue,
                        exchange=self._configuration.exchange,
                        routing_key=subscription.routing_key,
                    )

                    self._logger.info(
                        "Adding a Subscription for %s." % (subscription.queue)
                    )
                    # Configure our subscription to consume from the Queue
                    channel.basic.consume(
                        partial(
                            self._on_message, subscription.handler, subscription.queue
                        ),
                        subscription.queue,
                        no_ack=False,
                    )

                self._logger.info("Starting Consumer.")
                # Start consuming the queue, using the on_message callback.
                channel.start_consuming()

    def _on_message(self, handler: type, queue: str, msg: amqpstorm.Message):
        self._logger.info("Received Message from %s." % queue)

        payload = msg.body
        # If the message is of a known Content-Type, decode it automatically.
        if msg.content_type == "application/json":
            payload = Message.from_json(msg.body)

        self._logger.debug("Message Content: %s" % str(payload))

        try:
            self._logger.debug("Dispatching message to %s." % handler.__name__)

            self._logger.info(self._injector)
            impl = self._injector.get(handler)

            assert isinstance(impl, Handler)

            impl.handle_message(payload)

            self._logger.info(
                "%s completed without error, ACKing message." % handler.__name__
            )

            msg.ack()
        except RollbackException as e:
            self._logger.info("%s failed: %s." % (handler.__name__, str(e)))

            self._logger.info("%s failed, Rolling back..." % handler.__name__)

            if e.rollback_strategy == RollbackStrategy.RETRY_NOW:
                msg.nack(requeue=True)
            elif e.rollback_strategy == RollbackStrategy.RETRY_LATER:
                msg.reject(requeue=True)
            elif e.rollback_strategy == RollbackStrategy.QUARANTINE:
                raise NotImplementedError("RollbackStrategy.QUARANTINE")
            else:
                raise Exception("no rollback stragy")
        except Exception as e:
            self._logger.info("%s failed: %s." % (handler.__name__, str(e)))

            msg.reject(requeue=True)
