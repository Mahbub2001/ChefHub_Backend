from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Chef

class ChefAdmin(UserAdmin):
    model = Chef
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('bio', 'profile_picture', 'phone_number', 'home', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(Chef, ChefAdmin)
