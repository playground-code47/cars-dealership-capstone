from django.contrib import admin

from .models import CarMake, CarModel, Dealership

admin.site.register(Dealership)
admin.site.register(CarMake)
admin.site.register(CarModel)
