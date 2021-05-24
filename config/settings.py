import json
import os
import sys

APP_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(APP_ROOT_PATH, 'settings.json'), 'r+') as f:
    settings = json.loads(f.read())

BFX_DETS = settings['BFX']

# STATIC - DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING
if len(sys.argv) > 1 and sys.argv[1] == 'localhost':
    REDIS_HOST = 'localhost'
else:
    REDIS_HOST = 'redis-cluster-ip-service'

REDIS_PORT = 6379
REDIS_LOG_LIST = 'RYO_LOG_LIST'