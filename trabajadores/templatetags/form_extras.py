from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Añade clases CSS a un campo de formulario.
    Uso: {{ field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})