from .models import Sensor
import django_filters


class SensorFilter(django_filters.FilterSet):
    class Meta:
        model = Sensor
        fields = ["status", "object"]
