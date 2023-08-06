from selia_templates.custom_tags.components.base import GenericNode


def listattribute(parser, token):
    header = parser.parse(('attributevalue',))
    parser.delete_first_token()

    content = parser.parse(('endlistattribute'))
    parser.delete_first_token()
    return GenericNode(
        template_name='selia_templates/list/list_attribute.html',
        header=header,
        content=content)


def listtitle(parser, token):
    try:
        image = parser.parse(('endlistimage',))
        parser.delete_first_token()
    except:
        image = None

    title = parser.parse(('endlistheader', ))
    parser.delete_first_token()

    try:
        description = parser.parse(('endlisttitle', ))
        parser.delete_first_token()
    except:
        description = None

    return GenericNode(
        template_name='selia_templates/list/list_item_title.html',
        title=title,
        image=image,
        description=description)


def listsummary(parser, token):
    title = parser.parse(('summarycount',))
    parser.delete_first_token()

    count = parser.parse(('summarybuttons', 'endlistsummary'))
    tag = parser.next_token()

    buttons = None
    if tag.contents == 'summarybuttons':
        buttons = parser.parse(('endlistsummary', ))
        parser.delete_first_token()

    return GenericNode(
        template_name='selia_templates/list/list_item_summary.html',
        title=title,
        count=count,
        buttons=buttons)


def list_component(context, template_name, item_list, empty_message):
    context['template_name'] = template_name
    context['item_list'] = item_list
    context['empty_message'] = empty_message
    return context


def list_icon(item, size='5em'):
    return {'item': item, 'size':size}
