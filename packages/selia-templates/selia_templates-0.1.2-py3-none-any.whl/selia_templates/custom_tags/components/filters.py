def filter_bar(context, forms):
    context['forms'] = forms

    search_form = forms['search']
    search_field = search_form.fields['search']
    search_field = search_field.get_bound_field(search_form, 'search')

    if search_field.data:
        context['search'] = search_field.data
        context['clear'] = True

    context['form'] = {}
    filter_form = forms['filter']
    for field_name, field in filter_form._form.fields.items():
        bound_field = field.get_bound_field(filter_form._form, field_name)
        if bound_field.data:
            context['form'][field_name] = {
                'data': bound_field.data,
                'label': field.label
            }
            context['clear'] = True

    return context


def remove_form_fields(query, forms):
    query = query.copy()

    if 'filter' in forms:
        filter_form = forms['filter']
        filter_prefix = filter_form._form.prefix
        for field in filter_form._form.fields:
            if filter_prefix:
                field = '{}-{}'.format(filter_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    if 'search' in forms:
        search_form = forms['search']
        search_prefix = search_form.prefix
        for field in search_form.fields:
            if search_prefix:
                field = '{}-{}'.format(search_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    if 'order' in forms:
        order_form = forms['order']
        order_prefix = order_form.prefix
        for field in order_form.fields:
            if order_prefix:
                field = '{}-{}'.format(order_prefix, field)
            try:
                query.pop(field)
            except:
                pass

    return query.urlencode()


def is_own_checkbox(form):
    return {'form': form}
