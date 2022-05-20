from django.db import models
from django.conf import settings
from rules.contrib.models import RulesModel
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


def location_image_upload_handler(instance, filename) -> str:
    return f"location_image/{instance.id}/{filename}"


def object_image_upload_handler(instance, filename) -> str:
    return f"object_image/{instance.id}/{filename}"


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
    management_group = models.ForeignKey(
        Group,
        verbose_name=_("management group"),
        related_name="location_management_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view, change or delete this location."),
    )
    maintenance_group = models.ForeignKey(
        Group,
        verbose_name=_("maintenance group"),
        related_name="location_maintenance_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view this location."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ["status", "name"]
        indexes = [
            models.Index(fields=["owner", "management_group", "maintenance_group"]),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/location/{self.id}"

    @property
    def status_color(self) -> str:
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
    management_group = models.ForeignKey(
        Group,
        verbose_name=_("management group"),
        related_name="object_management_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view or update this object."),
    )
    maintenance_group = models.ForeignKey(
        Group,
        verbose_name=_("maintenance group"),
        related_name="object_maintenance_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view this object."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("object")
        verbose_name_plural = _("objects")
        ordering = ["status", "name"]
        indexes = [
            models.Index(fields=["owner", "management_group", "maintenance_group"]),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/object/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color


class Sensor(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("alert")
        AMBER = 20, _("warning")
        GREEN = 30, _("normal")

    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=object_image_upload_handler, blank=True, null=True
    )
    object = models.ForeignKey(
        Object,
        verbose_name=_("object"),
        related_name="sensor_object",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        _("status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    webhook_authorization = models.CharField(
        _("webhook authorization"), max_length=255, blank=True, null=True
    )
    webhook_payload = models.JSONField(_("webhook payload"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("sensor")
        verbose_name_plural = _("sensors")
        ordering = ["status", "name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/sensor/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color
