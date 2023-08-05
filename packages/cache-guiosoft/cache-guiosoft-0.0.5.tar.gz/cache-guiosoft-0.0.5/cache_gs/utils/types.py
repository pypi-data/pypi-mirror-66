def type_to_str(data_type):
    dt = str(data_type).split("'")
    if len(dt) != 3:
        raise ValueError('invalid data_type', data_type)

    return dt[1]


def str_to_type(str_type):
    if str_type in ['int', 'float', 'bool', 'str',
                    'datetime.datetime', 'datetime.date']:
        t = eval(str_type)
    else:
        t = None

    return t


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


def default_to(value, default='_'):
    return default if not isinstance(value, str) or not value else value
