from django import template
from selia_templates.custom_tags.components.base import ComplexNode


def tab(parser, token):
    content = parser.parse(('endtab',))
    parser.delete_first_token()

    try:
        _, url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    return ComplexNode(
        template_name='selia_templates/navbars/tab.html',
        content=content,
        url=url)
