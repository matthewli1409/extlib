import json

from redis import Redis

from settings.settings import REDIS_HOST, REDIS_PORT, REDIS_LOG_LIST


def log_msg(data, log_type='GENERIC', log_lvl='INFO'):
    """log helper"""
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    data_to_push = json.dumps({'logType': log_type, 'logLvl': log_lvl, 'data': data})
    r.lpush(REDIS_LOG_LIST, data_to_push)
