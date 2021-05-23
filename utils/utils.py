import sys

import pandas as pd
import requests
import slack

from config.settings import *
from log.log import errorslogger, logger


def log_info_msg(msg):
    """Log info to server-log server

    Args:
        msg {str} -- Message to log
    """
    if len(sys.argv) > 1 and sys.argv[1] == 'localhost':
        logger.info(msg)
    else:
        logger.info(requests.post(
            f'http://{SERVER_LOG_NAME}:{SERVER_LOG_PORT}/log/info', msg).content.decode('ascii'))


def log_error_msg(msg):
    """Log error to server-log server

    Args:
        msg {str} -- Message to log
    """
    if len(sys.argv) > 1 and sys.argv[1] == 'localhost':
        logger.error(msg)
        errorslogger.error(msg)
    else:
        errorslogger.error(requests.post(
            f'http://{SERVER_LOG_NAME}:{SERVER_LOG_PORT}/log/error', msg).content.decode('ascii'))


def to_camel_case(snake_str):
    """Transform snake case to camel case used in mongo

    Args:
        snake_str {str} -- string to transform
    """
    snake_str = snake_str.lower()
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def send_slack_msg(msg, title):
    """Slack helper function

    Arguments:
        msg {str} -- message to be sent
        title {str} -- title of message
    """
    client = slack.WebClient(SLACK_KEY)
    client.chat_postMessage(
        channel=SLACK_CHANNEL,
        icon_url='https://cdn.inprnt.com/thumbs/a2/0b/a20b43443f99849fcf5031393aedcea4@2x.jpg',
        parse='full',
        text=msg,
        username=title,
    )


def get_last_model_data(tail_points=5):
    """Get latest model data from model.csv

    Arguments:
        tail_points {int} -- how many points to print out from data csv
    """
    pd.set_option('display.max_columns', 50)
    pd.set_option('display.width', 500)
    df = pd.read_csv(os.path.join('data', 'model.csv'))
    df.set_index('dateTime', inplace=True)
    df = df.loc[:, (~df.columns.str.endswith('va_signal')) & (~df.columns.str.endswith('exp_std'))]
    df.drop(['rebal_inst', 'nav', 'rets', 'tx'], axis=1, inplace=True)
    print(df.tail(tail_points))
