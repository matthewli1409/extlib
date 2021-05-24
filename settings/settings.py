import sys

# STATIC - DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING
if len(sys.argv) > 1 and sys.argv[1] == 'localhost':
    REDIS_HOST = 'localhost'
else:
    REDIS_HOST = 'redis-cluster-ip-service'

REDIS_PORT = 6379
REDIS_LOG_LIST = 'RYO_LOG_LIST'
