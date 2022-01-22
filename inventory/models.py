from django.db import models
from django.conf import settings
from rules.contrib.models import RulesModel
import uuid
import pathlib
from common.models import Team
from django.utils.translation import gettext_lazy as _


def object_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"object_image/{file_name}{file_suffix}"


def location_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"location_image/{file_name}{file_suffix}"


class Location(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("alert")
        AMBER = 20, _("warning")
        GREEN = 30, _("normal")

    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=location_image_upload_handler, blank=True, null=True
    )
    address = models.TextField(_("address"), blank=True)
    latitude = models.FloatField(_("latitude"), blank=True, null=True)
    longitude = models.FloatField(_("longitude"), blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        _("status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        related_name="location_owner",
        on_delete=models.CASCADE,
        help_text=_("Owner can view, change or delete this location."),
    )
    management_team = models.ForeignKey(
        Team,
        verbose_name=_("management team"),
        related_name="location_management_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Team members can view, change or delete this location."),
    )
    maintenance_team = models.ForeignKey(
        Team,
        verbose_name=_("maintenance team"),
        related_name="location_maintenance_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Team members can view this location."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ["status", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/location/{self.id}"

    @property
    def get_status_color(self):
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color


class Object(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("alert")
        AMBER = 20, _("warning")
        GREEN = 30, _("normal")

    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=object_image_upload_handler, blank=True, null=True
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        related_name="object_location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(
        _("status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        related_name="object_owner",
        on_delete=models.CASCADE,
        help_text=_("Owner can view, change or delete this object."),
    )
    management_team = models.ForeignKey(
        Team,
        verbose_name=_("management team"),
        related_name="object_management_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Team members can view or update this object."),
    )
    maintenance_team = models.ForeignKey(
        Team,
        verbose_name=_("maintenance team"),
        related_name="object_maintenance_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Team members can view this object."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("object")
        verbose_name_plural = _("objects")
        ordering = ["status", "name"]

    def __str__(self):
        name = self.name
        if self.location:
            name = self.name + " @" + str(self.location)
        return name

    def get_absolute_url(self):
        return f"/object/{self.id}"

    @property
    def get_status_color(self):
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color
