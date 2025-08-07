from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration', 'course', 'semester', 'status', 'enrollment_date', 'created_by']
    list_filter = ['status', 'course', 'semester', 'enrollment_date', 'created_by']
    search_fields = ['name', 'registration', 'email']
    readonly_fields = ['uuid', 'enrollment_date', 'created_at', 'created_by', 'updated_at', 'updated_by']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('name', 'email')
        }),
        ('Informações Acadêmicas', {
            'fields': ('registration', 'course', 'semester', 'status')
        }),
        ('Auditoria', {
            'fields': ('uuid', 'created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('enrollment_date',),
            'classes': ('collapse',)
        }),
    )