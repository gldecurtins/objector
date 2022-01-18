from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from maintenance.models import Work
from .models import Location, Objekt


@receiver(post_save, sender=Work)
def update_status(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: objekt_update_status(instance))


def objekt_update_status(work_instance):
    objekt = Objekt.objects.get(id=work_instance.objekt.id)

    new_objekt_status = Objekt.Statuses.GREEN
    if Work.objects.filter(
        objekt=work_instance.objekt.id, status=Work.Statuses.OVERDUE
    ).exists():
        new_objekt_status = Objekt.Statuses.RED
    elif Work.objects.filter(
        objekt=work_instance.objekt.id, status=Work.Statuses.DUE
    ).exists():
        new_objekt_status = Objekt.Statuses.AMBER

    if objekt.status != new_objekt_status:
        objekt.status = new_objekt_status
        objekt.save()


@receiver(post_save, sender=Objekt)
def update_status(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    if instance.location:
        transaction.on_commit(lambda: location_update_status(instance))


def location_update_status(objekt_instance):
    location = Location.objects.get(id=objekt_instance.location.id)

    new_location_status = Location.Statuses.GREEN
    if Objekt.objects.filter(
        location=objekt_instance.location.id, status=Objekt.Statuses.RED
    ).exists():
        new_location_status = Location.Statuses.RED
    elif Objekt.objects.filter(
        location=objekt_instance.location.id, status=Objekt.Statuses.AMBER
    ).exists():
        new_location_status = Location.Statuses.AMBER

    if location.status != new_location_status:
        location.status = new_location_status
        location.save()
