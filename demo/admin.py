from django.contrib import admin
from .models import Temperature, ScannerTemperature


# Register your models here.
@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('temp', 'scanner_id', 'created', 'status')
    list_filter = ('status', 'created', 'scanner_id', 'publish')
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    ordering = ('status', 'created')


@admin.register(ScannerTemperature)
class ScannerTemperatureAdmin(admin.ModelAdmin):
    list_display = ('scanner_id', 'name', 'dept', 'created')
    search_fields = ('scanner_id', 'name', 'dept')
    date_hierarchy = 'created'
    raw_id_fields = ('user',)
    ordering = ('-created',)
