from app.config import settings
from redis import Redis

redis_client = Redis.from_url(
    url=settings.get_redis_url_async(),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=5,
)