from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['carmake', 'name', 'dealerid', 'Type', 'Year']
    list_filter = ['carmake', 'dealerid', 'Type', 'Year']
    search_fields = ['carmake', 'name']


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)