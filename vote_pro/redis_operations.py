import redis

def refresh_user_votes(redis_conn):
    """
    Refreshes user votes in Redis by setting remain_votes to 50 for all users.

    Args:
        redis_conn (redis.Redis): Redis connection object.
    """
    pipe = redis_conn.pipeline()
    users = redis_conn.keys("user:*")
    for user in users:
        pipe.hset(user, 'remain_votes', 50)
    pipe.execute()


def set_user_votes_to_zero(userId, redis_conn):
    """
    Sets user votes to zero in Redis for a specific user.

    Args:
        userId (str): The user ID for which votes need to be set to zero.
        redis_conn (redis.Redis): Redis connection object.
    """
    user_key = f"user:{userId}"
    redis_conn.hset(user_key, 'remain_votes', 0)