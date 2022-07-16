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