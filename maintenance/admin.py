from django.contrib import admin
from .models import Task, Journal, Trigger


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "object", "status", "due_at", "overdue_at")


class JournalAdmin(admin.ModelAdmin):
    list_display = ("object", "task", "notes", "labor_costs", "material_costs")


class TriggerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sensor",
        "status",
        "sensor_value",
        "condition",
        "amber_value",
        "red_value",
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Trigger, TriggerAdmin)
