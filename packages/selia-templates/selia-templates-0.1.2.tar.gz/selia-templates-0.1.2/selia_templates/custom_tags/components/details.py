from selia_templates.custom_tags.components.base import GenericNode


def detailitem(parser, token):
    header = parser.parse(('endhead',))
    parser.delete_first_token()

    content = parser.parse(('enddetailitem',))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/detail/detail_item.html',
        header=header,
        content=content)


def detailtitle(parser, token):
    try:
        image = parser.parse(('enddetailimage',))
        parser.delete_first_token()
    except:
        image = None

    title = parser.parse(('enddetailheader', ))
    parser.delete_first_token()

    try:
        description = parser.parse(('enddetailtitle', ))
        parser.delete_first_token()
    except:
        description = None

    return GenericNode(
        template_name='selia_templates/detail/detail_title.html',
        title=title,
        image=image,
        description=description)


def detailsection(parser, token):
    content = parser.parse(('enddetailsection',))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/detail/detail_section.html',
        content=content)


def detail_component(context, detail_template, object):
    context['detail_template'] = detail_template
    context['object'] = object
    return context


def detail_icon(item):
    return {'item': item}
