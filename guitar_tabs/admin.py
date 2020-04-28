from django.contrib import admin

from guitar_tabs.models import GuitarTabDetails, GuitarTab, Comment

admin.site.register(GuitarTabDetails)
admin.site.register(GuitarTab)
admin.site.register(Comment)
