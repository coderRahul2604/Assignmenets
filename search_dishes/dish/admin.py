from django.contrib import admin
from .models import Restaurant, Dish

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display=['name', 'location']
    search_fields = ['name']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display=['name', 'price']
    search_fields = ['name']
