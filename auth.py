import random

class KeyValueStore():
    """Basic Key Value store

    In production, you'd want to use something like memcached or redis,
    but for simplicity this app uses a python dict.
    """
    def __init__(self):
        self.kv_dict = {}

    def set(self, key, value, time=None):
        # In this simple example `time` does nothing, but if you are using
        # a proper KV store (memcached, redis, etc), then it will
        self.kv_dict[key] = value

    def get(self, key):
        return self.kv_dict.get(key)

class EmailCodeAuth():
    @classmethod
    def generate_random_string(cls, length=20, chars=None):
        if chars is None:
            chars = 'abcdefghijklmnopqrstuvwxyz'

        return ''.join(random.choice(chars) for _ in range(length))

    def __init__(self, kv_store):
        self.kv_store = kv_store

    def generate_code(self, email, expire_seconds=86400):
        code = self.generate_random_string()
        self.kv_store.set(code, email, time=expire_seconds)
        return code

    def validate_code(self, code):
        return self.kv_store.get(code)
