from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date', 'location', 'organizer')
    search_fields = ('event_name', 'organizer__user__username', 'location')
    list_filter = ('date', 'location')
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('event_name', 'description', 'date', 'location', 'organizer')
        }),
    )
