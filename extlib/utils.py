import datetime


def convert_dict_keys_from_ms_to_dt(dict):
    """Conver dictionary keys from ms to datetime

    Args:
        dict {dict}: Dictionary in question

    Returns:
        dict -- New dictionary with datetime as keys
    """
    new_dict = {}
    for key in dict:
        dt = datetime.datetime.fromtimestamp(float(key)/1000.0)
        new_key = f"{dt.year}, {dt.month}, {dt.day}"
        new_dict[new_key] = dict[key]
    return new_dict
