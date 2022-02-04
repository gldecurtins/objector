from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import Group
from common.models import Team


@receiver(post_delete, sender=Team)
def team_delete_group_receiver(sender, instance, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: team_delete_group(instance))


def team_delete_group(team_instance):
    Group.objects.filter(id=team_instance.group.id).delete()
