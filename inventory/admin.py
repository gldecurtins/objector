from django.contrib import admin
from .models import Location, Object, Sensor


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "status",
        "owner",
        "management_group",
        "maintenance_group",
    )
    list_editable = ("status",)


class ObjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "location",
        "status",
        "owner",
        "management_group",
        "maintenance_group",
    )
    list_editable = ("status",)


class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "object", "status")
    list_editable = ("status",)


admin.site.register(Location, LocationAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Sensor, SensorAdmin)
