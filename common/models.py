from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel
import uuid
import pathlib


class User(AbstractUser):
    pass


def team_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"team_image/{file_name}{file_suffix}"


class Team(RulesModel):
    group = models.OneToOneField(
        Group,
        verbose_name=_("group"),
        related_name="team_group",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(_("name"), max_length=80, unique=True)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=team_image_upload_handler, blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("owner"),
        related_name="team_owner",
        on_delete=models.CASCADE,
        help_text="Owner can view, change or delete this team.",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/team/{self.pk}"

    def update_or_create_group(self, *args, **kwargs):
        team_group, _ = Group.objects.update_or_create(
            id=self.pk,
            defaults={"name": self.name},
        )
        self.group = team_group

    def save(self, *args, **kwargs):
        self.update_or_create_group()
        return super().save(*args, **kwargs)
