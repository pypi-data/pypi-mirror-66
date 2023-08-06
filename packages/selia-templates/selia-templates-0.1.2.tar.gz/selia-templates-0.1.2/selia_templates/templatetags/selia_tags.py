from django import template
from django.utils.safestring import mark_safe

from dal_select2.widgets import Select2WidgetMixin

from selia_templates.custom_tags.components import lists
from selia_templates.custom_tags.components import details
from selia_templates.custom_tags.components import extra
from selia_templates.custom_tags.components import filters
from selia_templates.custom_tags.components import navbars

from selia_templates.custom_tags import json_data


register = template.Library()


register.tag('listattribute', lists.listattribute)
register.tag('listtitle', lists.listtitle)
register.tag('listsummary', lists.listsummary)
register.inclusion_tag(
    'selia_templates/list/list.html',
    name='list_component',
    takes_context=True)(lists.list_component)
register.inclusion_tag(
    'selia_templates/list/list_icon.html',
    name='list_icon')(lists.list_icon)

register.tag('detailitem', details.detailitem)
register.tag('detailtitle', details.detailtitle)
register.tag('detailsection', details.detailsection)
register.inclusion_tag(
    'selia_templates/detail/detail.html',
    name='detail_component',
    takes_context=True)(details.detail_component)
register.inclusion_tag(
    'selia_templates/detail/detail_icon.html',
    name='detail_icon')(details.detail_icon)

register.simple_tag(json_data.show_json, name='show_json')
register.simple_tag(json_data.parse_annotation_label, name='parse_annotation_label')

register.inclusion_tag(
    'selia_templates/modals/help.html',
    name='help_component',
    takes_context=True)(extra.help_component)
register.inclusion_tag(
    'selia_templates/modals/update.html',
    name='update_component',
    takes_context=True)(extra.update_component)
register.inclusion_tag(
    'selia_templates/detail/summary.html',
    name='summary_component',
    takes_context=True)(extra.summary_component)
register.inclusion_tag(
    'selia_templates/filters/filter.html',
    name='filter_component',
    takes_context=True)(extra.filter_component)
register.inclusion_tag(
    'selia_templates/modals/delete.html',
    name='delete_component',
    takes_context=True)(extra.delete_component)
register.inclusion_tag(
    'selia_templates/viewer.html',
    name='viewer_component',
    takes_context=True)(extra.viewer_component)
register.inclusion_tag(
    'selia_templates/create/create.html',
    name='create_component',
    takes_context=True)(extra.create_component)
register.inclusion_tag(
    'selia_templates/annotator.html',
    name='annotator_component',
    takes_context=True)(extra.annotator_component)
register.inclusion_tag(
    'selia_templates/select/selected_item.html',
    name='selected_item')(extra.selected_item)


register.tag('tab', navbars.tab)


register.simple_tag(filters.remove_form_fields, name='remove_form_fields')
register.inclusion_tag(
    'selia_templates/filters/filter_bar.html',
    name='filter_bar',
    takes_context=True)(filters.filter_bar)
register.inclusion_tag(
    'selia_templates/filters/is_own_checkbox.html',
    name='is_own_checkbox')(filters.is_own_checkbox)


@register.simple_tag
def autocomplete_media():
    extra_script = r'''
    <script>
      $(document).on('click', '.dropdown-menu .select2*', function(e) {
        e.stopPropagation();
      });
    </script>
    '''

    media = '''
    {select2_media}
    {extra_script}
    '''.format(
        select2_media=Select2WidgetMixin().media,
        extra_script=extra_script)

    return mark_safe(media)
