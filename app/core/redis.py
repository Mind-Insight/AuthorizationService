from redis.asyncio import Redis


class RedisConnection:
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        db: int = 0,
        decode_responses: bool = True,
    ):
        self.redis_url = redis_url
        self.db = db
        self.decode_responses = decode_responses
        self.redis: Redis | None = None

    async def __aenter__(self) -> Redis:
        if not self.redis:
            self.redis = Redis.from_url(
                self.redis_url,
                decode_responses=self.decode_responses,
            )
        return self.redis

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.redis:
            await self.redis.close()
            self.redis = None


redis_connection = RedisConnection()
