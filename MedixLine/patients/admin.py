from django.contrib import admin
from .models import Patient 


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'user_email',
        'date_of_birth',
        'gender',
        'phone_number',
        'address',
    )

    list_filter = (
        'gender',
    )

    search_fields = ('user__username', 'user__email')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'gender', 'date_of_birth'),
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address'),
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    
    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    get_full_name.short_description = 'Full Name'


admin.site.register(Patient, PatientAdmin)
