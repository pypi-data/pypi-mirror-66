import pycountry


def get_country_name(value):
    return pycountry.countries.lookup(value).name


def cut_pagination(range, page=1):
    length = len(range)
    if length < 6:
        return {
            'range': range,
            'pre_ellipsis': False,
            'post_ellipsis': False
        }

    lower_limit = max(0, page - 3)
    upper_limit = min(page + 2, length)

    return {
        'range': range[lower_limit: upper_limit],
        'pre_ellipsis': page > 3,
        'post_ellipsis': length - page > 2
    }
