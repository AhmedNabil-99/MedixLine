from django.contrib import admin
from .models import User
# Register your models here.

admin.site.site_header = 'MedixLine'
admin.site.site_title = 'MedixLine'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
            ),
    )
    ordering = ('username', 'email')
    

admin.site.register(User, UserAdmin)


