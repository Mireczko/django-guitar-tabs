from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (_('Personal info'), {'fields': ('nick','email',)}),
        (_('Status'), {'fields': ('is_active', 'is_staff')}),
        (_('Email change'), {'fields': ('pending_email',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Group'), {'fields': ('groups',)})

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nick',  'is_staff', 'groups'),
        }),
    )
    list_display = ('email', 'nick', 'is_staff')
    search_fields = ('email', 'nick',)
    ordering = ('email',)


# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
