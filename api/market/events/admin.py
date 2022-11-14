from django.contrib import admin
from events.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  # pragma nocover
    list_display = ['id', 'name', 'user_email', 'created_at']
    list_filter = ['name', 'user_email']
    ordering = ['name', 'user_email', 'created_at']

    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=...) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=...) -> bool:
        return False
