from redis import Redis
from config import settings
from rq import Queue

REDIS_QUEUES = ["default","file","email","sms"]

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD
)

queues = {
    q:Queue(
        q,
        connection=redis
    )
    for q in REDIS_QUEUES
}

get_queue = lambda queue: queues.get(queue, None)