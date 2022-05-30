from .models import Task, Journal
import django_filters


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ["object__location", "object", "status"]


class JournalFilter(django_filters.FilterSet):
    class Meta:
        model = Journal
        fields = ["object__location", "object"]
