from django.template import Node
from django.template.loader import get_template


class GenericNode(Node):
    def __init__(self, template_name=None, **kwargs):
        self.template_name = template_name
        self.data = kwargs

    def render(self, context):
        template = get_template(self.template_name)
        template_context = {
            key: value.render(context)
            for key, value in self.data.items()
            if value is not None
        }

        return template.render(template_context)


class ComplexNode(Node):
    def __init__(self, template_name=None, **kwargs):
        self.template_name = template_name
        self.data = kwargs

    def render(self, context):
        template = get_template(self.template_name)

        template_context = {}
        for key, value in self.data.items():
            if value is None:
                continue

            try:
                template_context[key] = value.render(context)
            except:
                template_context[key] = context[value]

        template_context['request'] = context['request']
        return template.render(template_context)
