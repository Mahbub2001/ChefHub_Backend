from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'chef', 'creation_date')
    search_fields = ('title', 'chef__user__username')
    list_filter = ('creation_date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'chef', 'description', 'ingredients', 'instructions', 'image_url')
        }),
        ('Dates', {
            'fields': ('creation_date',)
        }),
    )
    readonly_fields = ('creation_date',)
