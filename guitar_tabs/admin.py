from django.contrib import admin

from guitar_tabs.models import  GuitarTab, Comment

admin.site.register(GuitarTab)
admin.site.register(Comment)
