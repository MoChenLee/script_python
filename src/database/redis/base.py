import redis

from src.database import redis_config


class Redis():
    def __init__(self):
        self.r = self.connect()

    def connect(self):
        redis_pool = redis.ConnectionPool(**redis_config["test"])
        return redis.StrictRedis(connection_pool=redis_pool)


