from django.contrib import admin
from .models import Temperature


# Register your models here.
@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'temp', 'user', 'scanner_id', 'created', 'status')
    list_filter = ('status', 'created', 'scanner_id', 'publish')
    search_fields = ('title', 'body')
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    ordering = ('status', 'created')