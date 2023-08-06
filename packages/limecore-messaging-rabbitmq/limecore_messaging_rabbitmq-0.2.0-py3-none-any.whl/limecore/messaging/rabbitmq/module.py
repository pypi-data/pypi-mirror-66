from injector import Module as _Module, provider, singleton
from limecore.core.configuration import Configuration
from limecore.messaging.api import Publisher, Subscriber

from .configuration import Configuration as RabbitMQConfiguration
from .publisher import Publisher as RabbitMQPublisher
from .subscriber import Subscriber as RabbitMQSubscriber


class Module(_Module):
    @singleton
    @provider
    def provide_configuration(
        self, configuration: Configuration
    ) -> RabbitMQConfiguration:
        rabbitmq_configuration = configuration.section(
            "limecore", "messaging", "rabbitmq"
        )

        return RabbitMQConfiguration(
            exchange=rabbitmq_configuration.get_string("exchange") or "amqp",
            host=rabbitmq_configuration.get_string("host") or "localhost",
            password=rabbitmq_configuration.get_string("password") or "guest",
            prefetch_count=rabbitmq_configuration.get_string("prefetch_count") or 2,
            user=rabbitmq_configuration.get_string("password") or "guest",
        )

    @provider
    def provide_publisher(self) -> Publisher:
        return self.__injector__.create_object(RabbitMQPublisher)

    @provider
    def provide_subscriber(self) -> Subscriber:
        return self.__injector__.create_object(RabbitMQSubscriber)
