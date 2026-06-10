from django.contrib import admin
from .models import Visitor, Blacklist

admin.site.register(Visitor)
admin.site.register(Blacklist)
