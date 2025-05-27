from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
    model = UserAccount
    list_display = ( 'email', 'role', 'is_admin', 'name', 'date_joined', 'last_login', 'is_verified')
    list_filter = ('role', 'is_admin', 'is_verified', 'date_joined')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('name', 'role', 'is_admin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('name', 'role', 'is_admin')}),
    )

admin.site.register(UserAccount, UserAccountAdmin)
