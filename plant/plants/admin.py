from django.contrib import admin
from .models import Plant

class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'species')
    search_fields = ['name']

admin.site.register(Plant, PlantAdmin)