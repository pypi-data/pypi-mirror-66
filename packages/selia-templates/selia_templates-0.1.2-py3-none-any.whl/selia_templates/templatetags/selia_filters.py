from django import template

from selia_templates.custom_tags import utils
from selia_templates.custom_tags import json_data
from selia_templates.custom_tags import urls


register = template.Library()


register.filter('get_country_name', utils.get_country_name)
register.filter('update_metadata', json_data.update_metadata, is_safe=True)
register.filter('is_not_trivial_schema', json_data.is_not_trivial_schema)
register.filter('remove_fields', urls.remove_fields, is_safe=True)
register.filter('add_chain', urls.add_chain, is_safe=True)
register.filter('add_fields', urls.add_fields, is_safe=True)
register.filter('remove_option', urls.remove_option)
register.filter('cut_pagination', utils.cut_pagination)
