import datetime

from redis import Redis


def get_strat_aum_redis(strat, host, port):
    """Get strat aum from redis

    Arguments:
        fund {str} -- strat name to pull aum for
        host {str} -- redis host
        port {int} -- redis port

    Returns:
        dict -- aum in $ normally, datetime
    """
    r = Redis(host=host, port=port, decode_responses=True)
    data = r.hgetall(f'{strat}_aum')
    data['aum'] = float(data.get('aum'))
    data['dateTime'] = datetime.datetime.strptime(data.get('dateTime'), '%Y-%m-%d %H:%M:%S')
    return data


def get_fund_aum_redis(fund, host, port):
    """Get fund aum from redis

    Arguments:
        fund {str} -- fund name to pull aum for
        host {str} -- redis host
        port {int} -- redis port

    Returns:
        dict -- aum in $ normally, datetime
    """
    r = Redis(host=host, port=port, decode_responses=True)
    data = r.hgetall(f'{fund}_aum')
    data['aum'] = float(data.get('aum'))
    data['dateTime'] = datetime.datetime.strptime(data.get('dateTime'), '%Y-%m-%d %H:%M:%S')
    return data


def get_tgt_wgt_redis(strat, host, port):
    """Get target weight from redis

    Arguments:
        fund {str} -- fund name to pull taget weight for
        host {str} -- redis host
        port {int} -- redis port

    Returns:
        float -- target weight, datetime
    """
    r = Redis(host=host, port=port, decode_responses=True)
    data = r.hgetall(f'{strat}_tgt_wgt')
    data['weight'] = float(data.get('weight'))
    data['dateTime'] = datetime.datetime.strptime(data.get('dateTime'), '%Y-%m-%d %H:%M:%S')
    return data
