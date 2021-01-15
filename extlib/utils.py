from datetime import datetime, timezone


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
