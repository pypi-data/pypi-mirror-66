from django import forms, template

register = template.Library()


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)
