from django.contrib import admin

from .models import Rule, Task

admin.site.register(Rule)
admin.site.register(Task)