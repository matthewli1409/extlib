import json

from redis import Redis

from config.settings import REDIS_HOST, REDIS_PORT, REDIS_LOG_LIST


def log_msg(log_type, data, log_lvl='INFO'):
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    data_to_push = json.dumps({'logType': log_type, 'logLvl': log_lvl, 'data': data})
    r.lpush(REDIS_LOG_LIST, data_to_push)
