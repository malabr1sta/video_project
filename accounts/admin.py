from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models as accounts_models


@admin.register(accounts_models.User)
class UserAdmin(BaseUserAdmin):
    # Поля для отображения и редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    list_display = ['id', 'username', 'is_staff']
    list_display_links = ['id']
    list_filter = ['is_staff']
    search_fields = ['id', 'username']
    readonly_fields = ('id', 'is_superuser')
