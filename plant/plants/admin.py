from django.contrib import admin

from .models import Plant, PlantFamily, Watering


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "species")
    search_fields = ["name"]


@admin.register(Watering)
class Watering(admin.ModelAdmin):
    list_display = ("id", "litres", "watering_date")


@admin.register(PlantFamily)
class PlantFamilyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
