from django.db import models
from django.conf import settings
from rules.contrib.models import RulesModel
import uuid
import pathlib
from common.models import Team


def objekt_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"objekt_image/{file_name}{file_suffix}"


def location_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"location_image/{file_name}{file_suffix}"


class Location(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, "Alert"
        AMBER = 20, "Warning"
        GREEN = 30, "Good"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=location_image_upload_handler, blank=True, null=True
    )
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Owner can view, change or delete this location.",
    )
    management_team = models.ForeignKey(
        Team,
        related_name="location_management_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Team members can view, change or delete this location.",
    )
    maintenance_team = models.ForeignKey(
        Team,
        related_name="location_maintenance_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Team members can view this location.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
        RED = 10, "Alert"
        AMBER = 20, "Warning"
        GREEN = 30, "Good"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=objekt_image_upload_handler, blank=True, null=True
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.PositiveSmallIntegerField(
        choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Owner can view, change or delete this object.",
    )
    management_team = models.ForeignKey(
        Team,
        related_name="objekt_management_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Team members can view or update this object.",
    )
    maintenance_team = models.ForeignKey(
        Team,
        related_name="objekt_maintenance_team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Team members can view this object.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
