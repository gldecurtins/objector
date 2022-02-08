from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from maintenance.models import Task
from .models import Location, Object, Sensor


@receiver(post_save, sender=Object)
def object_update_status_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    if instance.location:
        transaction.on_commit(lambda: object_update_status(instance))


def object_update_status(object_instance):
    location = Location.objects.get(id=object_instance.location.id)

    new_location_status = Location.Statuses.GREEN
    if Object.objects.filter(
        location=object_instance.location.id, status=Object.Statuses.RED
    ).exists():
        new_location_status = Location.Statuses.RED
    elif Object.objects.filter(
        location=object_instance.location.id, status=Object.Statuses.AMBER
    ).exists():
        new_location_status = Location.Statuses.AMBER

    if location.status != new_location_status:
        location.status = new_location_status
        location.save()


@receiver(post_save, sender=Task)
def task_update_status_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: task_update_status(instance))


def task_update_status(task_instance):
    object = Object.objects.get(id=task_instance.object.id)

    new_object_status = Object.Statuses.GREEN
    if Task.objects.filter(
        object=task_instance.object.id, status=Task.Statuses.OVERDUE
    ).exists():
        new_object_status = Object.Statuses.RED
    elif Task.objects.filter(
        object=task_instance.object.id, status=Task.Statuses.DUE
    ).exists():
        new_object_status = Object.Statuses.AMBER

    if object.status != new_object_status:
        object.status = new_object_status
        object.save()


@receiver(post_save, sender=Sensor)
def sensor_update_status_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: sensor_update_status(instance))


def sensor_update_status(sensor_instance):
    object = Object.objects.get(id=sensor_instance.object.id)

    new_object_status = Object.Statuses.GREEN
    if Sensor.objects.filter(
        object=sensor_instance.object.id, status=Sensor.Statuses.RED
    ).exists():
        new_object_status = Object.Statuses.RED
    elif Task.objects.filter(
        object=sensor_instance.object.id, status=Sensor.Statuses.AMBER
    ).exists():
        new_object_status = Object.Statuses.AMBER

    if object.status != new_object_status:
        object.status = new_object_status
        object.save()
