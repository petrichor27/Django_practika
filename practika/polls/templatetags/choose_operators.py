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
        return True
    return False

@register.simple_tag()
def check_list(arg):
    if type(arg) == list:
        print('t')
        return True
    print('f')
    return False

@register.simple_tag()
def make_values_list(arg):
    if arg[0] == '[':
        arg1 = arg.replace('[','')
        arg1 = arg1.replace(']','')
        arg1 = arg1.replace("'",'')
        res = []
        t = ''
        for i in range(len(arg1)):
            if arg1[i] != ',':
                if arg1[i] != ' ':
                    t += arg1[i]
            else:
                res.append(t)
                t = ''
        res.append(t)
        return res
    else: return [arg]
