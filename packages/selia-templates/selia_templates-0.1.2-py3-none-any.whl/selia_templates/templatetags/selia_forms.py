from django import template
from django.utils.translation import gettext as _
from django.utils.html import mark_safe

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from widget_tweaks.templatetags.widget_tweaks import add_class as widget_tweaks_add_class

register = template.Library()


FORM_ICONS = {
    'exact': '<i class="fas fa-equals"></i>',
    'iexact':'<i class="fas fa-equals"></i>',
    'in': '<i class="fas fa-list-ol"></i>',
    'lt': '<i class="fas fa-less-than"></i>',
    'gt': '<i class="fas fa-greater-than"></i>',
    'gte': '<i class="fas fa-greater-than-equal"></i>',
    'lte': '<i class="fas fa-less-than-equal"></i>',
    'icontains': '<i class="fas fa-font"></i>',
    'contains': '<i class="fas fa-font"></i>',
    'istartswith': '<i class="fas fa-font"></i>',
    'startswith': '<i class="fas fa-font"></i>',
    'iendswith': '<i class="fas fa-font"></i>',
    'endswith': '<i class="fas fa-font"></i>',
    'regex': '<i class="fas fa-terminal"></i>',
    'iregex': '<i class="fas fa-terminal"></i>',
}


@register.filter(name='selia_form')
def selia_form(form, label_class="", field_class=""):
    return as_crispy_form(
        form,
        template_pack='bootstrap4',
        label_class=label_class,
        field_class=field_class)


@register.filter(name='add_class')
def add_class(form, css_class):
    return widget_tweaks_add_class(form, css_class)


@register.filter(name='selia_filter', is_safe=True)
def selia_filter(form, label):
    widget = form.field.widget

    custom_attrs = ' form-control'
    if widget.input_type == 'select':
        custom_attrs += ' custom-select'

    if widget.input_type == 'file':
        custom_attrs = 'custom-file-input'

    widget_attrs = widget.attrs.get('class', '')
    class_for_html = widget_attrs + custom_attrs

    input_html = form.as_widget(attrs={'class': class_for_html})

    try:
        lookup_expr = form.html_name.split('__')[-1]
        icon = FORM_ICONS.get(lookup_expr, FORM_ICONS['exact'])
    except:
        icon = FORM_ICONS['exact']

    prepend_html = '''
    <div class="input-group-prepend">
        <span class="input-group-text" id="{prepend_id}">
            {prepend_icon}
        </span>
    </div>
    '''.format(
        prepend_id=form.html_name + '_prepend',
        prepend_icon=icon
    )

    append_html = '''
    <div class="input-group-append">
        <button type="submit" class="btn btn-outline-success" type="button" id="{append_id}">
            {append_icon} <i class="fas fa-plus"></i>
        </button>
    </div>
    '''.format(
        append_id=form.html_name + '_append',
        append_icon=_('add')
    )

    help_text_html = '''
    <small id="{help_text_id}" class="form-text text-muted">{help_text}</small>
    '''.format(
        help_text_id=form.html_name + '_help_text',
        help_text=form.help_text
    )

    if label:
        label_html = form.label_tag(contents=label)
    elif label is None:
        label_html = ''
    else:
        label_html = form.label_tag()

    form_html = '''
      <div class="form-group w-100">
        <small>{label_html}</small>
        <div class="input-group">
            {prepend_html}
            {input_html}
            {append_html}
        </div>
        {help_text_html}
      </div>
    '''
    form_html = form_html.format(
        label_html=label_html,
        prepend_html=prepend_html,
        input_html=input_html,
        append_html=append_html,
        help_text_html=help_text_html)

    return mark_safe(form_html)


@register.inclusion_tag('selia_templates/forms/bootstrap_form.html')
def bootstrap_form(form, disabled=False):
    if disabled:
        form.field.widget.attrs['readonly'] = True
    return {'form': form}
