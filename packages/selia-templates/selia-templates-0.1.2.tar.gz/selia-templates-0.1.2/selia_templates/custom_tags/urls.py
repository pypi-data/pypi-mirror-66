import re


def add_fields(query, fields):
    query_copy = query.copy()
    try:
        fields = fields.split('&')
    except:
        return query_copy.urlencode()

    for field in fields:
        try:
            key, value = field.split("=")
            query_copy[key] = value
        except:
            pass

    return query_copy.urlencode()


def remove_fields(query, fields):
    fields = fields.split('&')
    query = query.copy()

    for field in fields:
        try:
            query.pop(field)
        except KeyError:
            pass

    return query.urlencode()


def add_chain(query, view_name):
    query_copy = query.copy()
    query_copy['chain'] = '{previous}|{new}'.format(
        previous=query.get('chain', ''),
        new=view_name)
    return query_copy.urlencode()


def remove_option(value, field):
    regex = r'({}=)([^&]+)'.format(field)
    result = re.sub(regex, r'\1', value)
    return result
