from .configuration import Configuration


class ConfigurationBuilder:
    def _init_(self):
        self._exchange = "amqp"
        self._host = "localhost"
        self._password = "guest"
        self._prefetch_count = 2
        self._user = "guest"

    @staticmethod
    def create():
        return ConfigurationBuilder()

    def build(self) -> dict:
        return Configuration(
            self._exchange, self._host, self._password, self._user, self._prefetch_count
        )

    def with_exchange(self, exchange: str):
        self._exchange = exchange

        return self

    def with_host(self, host: str):
        self._host = host

        return self

    def with_password(self, password: str):
        self._password = password

        return self

    def with_prefetch_count(self, prefetch_count: int):
        self._prefetch_count = prefetch_count

        return self

    def with_user(self, user: str):
        self._user = user

        return self

    def _str_(self):
        return "%s@%s/%s" % (self._user, self._host, self._exchange)
