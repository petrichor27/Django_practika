# import os
from django.conf import settings
from django import template
# from six.moves import configparser
from polls.models import *

# site_parser = configparser.ConfigParser()
# site_parser.read(os.path.join(settings.BASE_DIR, "init.ini"))

register = template.Library()

#{{ somevariable|cut:"0" }}
#{% load choose_operators %}

@register.simple_tag()
def choose_operators(arg):
    return Dictionaries.get_operators(arg)


@register.simple_tag()
def choose_values(arg,type1,type2):
    return Dictionaries.get_values(arg,type1,type2)


@register.simple_tag()
def check_attribute(arg, type1, type2):
    if arg == 'Тип задания 2' and type1 or arg == 'Тип задания 3' and type1 and type2 or arg != 'Тип задания 2' and arg != 'Тип задания 3':
        t = Task.objects.all()
        a = []
        for i in t:
            a.append(i.attribute)
        if arg in a:
            return False
        return True
    return False