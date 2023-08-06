"""
   SDC Redis helper module
"""
import os
import redis


class RedisHelper:
    """
       Redis helper class
    """
    redis_conn = None

    def __init__(self):
        try:
            self.redis_conn = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=os.getenv('REDIS_PORT', '6379')
            )
        except redis.ConnectionError as exception:
            print(exception)

    def __del__(self):
        self.redis_conn.connection_pool.disconnect()

    def redis_set(self, *, key: str, value, expiry: int = None):
        """
            Set a Redis key with the specified value

            args:
                key (str): The Redis key
                value (str): The value to set
                expiry (int): A TTL for the specified key
        """
        self.redis_conn.set(key, value, expiry)

    def redis_get(self, *, key: str):
        """
            Get a Redis key

            args:
                key (str): The Redis key

            return:
                value : Returns the value for the specified key

        """
        return self.redis_conn.get(key)

    def redis_delete(self, *, key: str):
        """
            Delete a Redis key

            args:
                key (str): The Redis key

        """
        self.redis_conn.delete(key)
