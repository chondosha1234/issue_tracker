from django.template import Library

register = Library()

@register.filter(name='is_instance')
def is_instance(value, model_class):
    return isinstance(value, model_class)
