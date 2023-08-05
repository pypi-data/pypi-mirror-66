import logging
from logging import config as logging_config
import os
from dotenv import load_dotenv
logger = logging.getLogger()


def init_app():
    global logger
    if not load_dotenv(override=False):
        logger.error('Could not find any .env file. The module will depend on system env only')

    app_logging_config = {
        'version': 1,
        'loggers': {
            '': {  # root logger
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'handlers': ['console'],
            },
        },
        'handlers': {
            'console': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'formatter': 'info',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'formatters': {
            'info': {
                'format': '%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s'
            }
        },
    }

    logging_config.dictConfig(app_logging_config)
    logger = logging.getLogger()

    logger.info("Load module = {}, environment={}, region={}\n".format(
        os.environ.get('APP_NAME'), os.environ.get('ENVIRONMENT'), os.environ.get('REGION')))


if __name__ == 'redisconnection':
    init_app()


from redisconnection import redis_connection





