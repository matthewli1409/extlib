from datetime import datetime, timezone, timedelta


def convert_dict_keys_from_ms_to_dt(dict_data):
    """Conver dictionary keys from ms to datetime

    Args:
        dict_data {dict}: Dictionary in question

    Returns:
        dict -- New dictionary with datetime as keys
    """
    new_dict = {}
    for key in dict_data:
        dt = datetime.fromtimestamp(float(key) / 1000.0, tz=timezone.utc)
        new_key = f"{dt.year}, {dt.month}, {dt.day}"
        new_dict[new_key] = dict_data[key]
    return new_dict


def get_benchmark_dates(cur_date):
    """Function returns the DTD, WTD, MTD, YTD starting dates

    Args:
        cur_date {datetime} -- date to be benchmarked against

    Returns:
        DTD, WTD, MTD, YTD dates
    """
    dtd_start = cur_date - timedelta(days=1)
    wtd_start = cur_date - timedelta(cur_date.weekday() + 1)
    mtd_start = cur_date.replace(day=1) - timedelta(days=1)
    ytd_start = cur_date.replace(month=1)
    ytd_start = ytd_start.replace(day=1) - timedelta(days=1)
    return dtd_start, wtd_start, mtd_start, ytd_start


def snake_to_camel(snake_str):
    """Transform snake case to camel case used in mongo

    Args:
        snake_str {str} -- string to transform
    """
    snake_str = snake_str.lower()
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])
