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
