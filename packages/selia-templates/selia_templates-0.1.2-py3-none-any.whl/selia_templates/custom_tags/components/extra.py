import uuid


def help_component(context, help_template):
    context['help_template'] = help_template
    return context


def update_component(context, update_template, form):
    context['update_template'] = update_template
    context['form'] = form
    return context


def summary_component(context, summary_template, object):
    context['summary_template'] = summary_template
    context['object'] = object
    return context


def filter_component(context, template, forms):
    context['template'] = template
    context['forms'] = forms
    return context


def delete_component(context, object):
    context['object'] = object
    return context


def viewer_component(context, viewer_template, object):
    context['viewer_template'] = viewer_template
    context['object'] = object
    return context


def create_component(context, create_template, form):
    context['create_template'] = create_template
    context['form'] = form
    return context


def annotator_component(context, annotator_template, item, annotation_list, mode):
    context['annotator_template'] = annotator_template
    context['annotation_list'] = annotation_list
    context['item'] = item
    context['mode'] = mode
    return context


def selected_item(template, item, label):
    random_id = uuid.uuid4().hex.lower()[0:8]
    full_template_name = 'selia/select_list_items/{name}.html'
    return {
        'template': full_template_name.format(name=template),
        'item': item,
        'id': random_id,
        'label': label
    }
