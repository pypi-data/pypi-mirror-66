from django.template.loader import get_template
from django.utils.translation import gettext as _
from django.utils.html import format_html


def update_metadata(form, metadata):
    form.update_metadata(metadata)


def is_not_trivial_schema(schema):
    if schema is None:
        return False

    if 'required' not in schema:
        return False

    return len(schema['required']) != 0


def show_json(data):
    return parse_json_value(data, 0)


def parse_annotation_label(data):
    header_level = 'h6'
    div_class = 'row'
    header_class = 'text-gray-dark text-muted mb-0'

    headers = [
        '''<div class="{div_class}">
                <{header_level} class="{header_class}">{value}</{header_level}>
           </div>'''.format(
               key=key.capitalize(),
               value=parse_json_value(value, 0),
               header_level=header_level,
               header_class=header_class,
               div_class=div_class)
        for key, value in sorted(data.items())]

    return format_html(''.join(headers))


def parse_json_object(data, level):
    if level == 0:
        div_class = 'd-block mr-3 mb-3 bg-light'
    else:
        div_class = 'd-block ml-4'

    template = get_template('selia_templates/widgets/json_object.html')

    context = {
        'data': {
            key: parse_json_value(value, level + 1)
            for key, value in sorted(data.items())
        },
        'class': div_class
    }

    return template.render(context)


def parse_json_list(data, level):
    bullets = [
        '<li>{}</li>'.format(parse_json_value(value, level + 1))
        for value in data
    ]

    return '<ul>{}</ul>'.format(''.join(bullets))


def parse_json_string(data):
    return '{}'.format(data)


def parse_json_number(data):
    return '{}'.format(data)


def parse_json_boolean(data):
    if data:
        response = _('yes')
    else:
        response = _('no')

    return '{}'.format(response)


def parse_json_null():
    return ''


def parse_json_value(data, level):
    if isinstance(data, dict):
        return parse_json_object(data, level)

    if isinstance(data, (list, tuple)):
        return parse_json_list(data, level)

    if isinstance(data, bool):
        return parse_json_boolean(data)

    if isinstance(data, str):
        return parse_json_string(data)

    if isinstance(data, (int, float)):
        return parse_json_number(data)

    return parse_json_null()
