from django import template
from importlib import import_module
from django.contrib.auth import get_user_model
from issues.models import Issue, Project
import sys

User = get_user_model()

register = template.Library()

@register.filter(name='is_instance')
def is_instance(value, class_str):
    model_class = getattr(sys.modules[__name__], class_str)
    return isinstance(value, model_class)

@register.filter(name='get')
def get(value, arg):
    return value[arg]
