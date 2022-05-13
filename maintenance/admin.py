from django.contrib import admin
from .models import Task, Journal


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "object", "status", "due_at", "overdue_at")


class JournalAdmin(admin.ModelAdmin):
    list_display = ("object", "task", "notes", "labor_costs", "material_costs")


admin.site.register(Task, TaskAdmin)
admin.site.register(Journal, JournalAdmin)
