class Configuration:
    def __init__(
        self,
        exchange: str = "amqp",
        host: str = "localhost",
        password: str = "guest",
        user: str = "guest",
        prefetch_count: int = 2,
    ):
        self.exchange = exchange
        self.host = host
        self.password = password
        self.prefetch_count = prefetch_count
        self.user = user
