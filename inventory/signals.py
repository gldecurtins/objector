from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from maintenance.models import Work
from .models import Location, Object


@receiver(post_save, sender=Work)
def update_status(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: object_update_status(instance))


def object_update_status(work_instance):
    object = Object.objects.get(id=work_instance.object.id)

    new_object_status = Object.Statuses.GREEN
    if Work.objects.filter(
        object=work_instance.object.id, status=Work.Statuses.OVERDUE
    ).exists():
        new_object_status = Object.Statuses.RED
    elif Work.objects.filter(
        object=work_instance.object.id, status=Work.Statuses.DUE
    ).exists():
        new_object_status = Object.Statuses.AMBER

    if object.status != new_object_status:
        object.status = new_object_status
        object.save()


@receiver(post_save, sender=Object)
def update_status(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    if instance.location:
        transaction.on_commit(lambda: location_update_status(instance))


def location_update_status(object_instance):
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
