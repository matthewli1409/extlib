import json

from redis import Redis

from settings import REDIS_HOST, REDIS_PORT, REDIS_LOG_LIST


def log_generic_msg(data, log_lvl='INFO'):
    """log helper for generic message"""
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    data_to_push = json.dumps({'logType': 'GENERIC', 'logLvl': log_lvl, 'data': str(data)})
    r.lpush(REDIS_LOG_LIST, data_to_push)


def log_error_msg(data, log_lvl='ERROR'):
    """log helper for error message"""
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    data_to_push = json.dumps({'logType': 'ERROR', 'logLvl': log_lvl, 'data': str(data)})
    r.lpush(REDIS_LOG_LIST, data_to_push)


def log_execution_msg(data, log_lvl='INFO'):
    """log helper for execution message"""
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    data_to_push = json.dumps({'logType': 'EXECUTION', 'logLvl': log_lvl, 'data': str(data)})
    r.lpush(REDIS_LOG_LIST, data_to_push)
