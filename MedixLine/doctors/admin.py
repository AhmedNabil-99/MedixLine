from django.contrib import admin
from doctors.models import Specialization, Doctor, WorkingDay,Rating
from django.utils.html import format_html


# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',                
        'email',
        'specialization',      
        'is_confirmed',        
        'phone_number',        
        'average_rating',      
        'gender',              
        'start_time',          
        'end_time',            
    )

    list_filter = (
        'specialization',     
        'is_confirmed',       
        'gender',             
        'working_days', 
    )

    search_fields = ('user__username', 'user__email')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'gender', 'date_of_birth'),
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address'),
        }),
        ('Professional Information', {
            'fields': ('specialization', 'working_days', 'start_time', 'end_time', 'duration', 'price'),
        }),
        ('Profile and IDs', {
            'fields': ('profile_picture', 'national_id', 'syndicate_id'),
        }),
        ('Documents', {
            'fields': ('profile_picture_preview','national_id_preview', 'syndicate_id_preview'),
        }),
        ('Verification and Status', {
            'fields': ('is_confirmed', 'average_rating'),
        }),
    )

    def email(self, obj):
        return obj.user.email
    
    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    get_full_name.short_description = 'Full Name'

    readonly_fields = ('profile_picture_preview', 'national_id_preview', 'syndicate_id_preview')

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.profile_picture.url)
        return "No Image"
    
    def national_id_preview(self, obj):
        if obj.national_id:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.national_id.url)
        return "No Image"
    
    def syndicate_id_preview(self, obj):
        if obj.syndicate_id:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.syndicate_id.url)
        return "No Image"
    

admin.site.register(Specialization)  
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(WorkingDay)
admin.site.register(Rating)