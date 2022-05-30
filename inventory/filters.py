from .models import Location, Object, Sensor
import django_filters


class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Location
        fields = ["status"]


class ObjectFilter(django_filters.FilterSet):
    class Meta:
        model = Object
        fields = ["location", "status"]


class SensorFilter(django_filters.FilterSet):
    class Meta:
        model = Sensor
        fields = ["object__location", "object", "status"]
