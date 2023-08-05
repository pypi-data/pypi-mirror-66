from redisconnection import redis_connection, logger


def test_connection():
    rd = redis_connection.RedisConnection()
    conn = rd.connection
    rd.close_connection()


if __name__ == '__main__':
    test_connection()




