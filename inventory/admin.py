from django.contrib import admin
from .models import Location, Object, Sensor

admin.site.register(Location)
admin.site.register(Object)
admin.site.register(Sensor)