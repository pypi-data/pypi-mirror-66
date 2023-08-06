from crispy_forms import layout as crispy_forms_layout


class Layout(crispy_forms_layout.Layout):
    pass


class HTML(crispy_forms_layout.HTML):
    pass


class Div(crispy_forms_layout.Div):
    """
    It wraps fields inside a ``<div>`` element.
    You can set ``css_id`` for element id and ``css_class`` for a element
    class names.
    Example:
    .. sourcecode:: python
        Div('form_field_1', 'form_field_2', css_id='div-example',
            css_class='divs')
    """
    template = "%s/layout/div.html"


class Empty(crispy_forms_layout.Div):
    """
    It wraps fields inside a ``<div>`` element.
    You can set ``css_id`` for element id and ``css_class`` for a element
    class names.
    Example:
    .. sourcecode:: python
        Div('form_field_1', 'form_field_2', css_id='div-example',
            css_class='divs')
    """
    template = "%s/layout/empty.html"
