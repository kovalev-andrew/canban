from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'user']
    search_fields = ['title', 'description', 'user__email', 'user__username']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_at', 'updated_at']

