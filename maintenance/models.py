from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel
from inventory.models import Object, Sensor
import uuid
import pathlib


def journal_image_upload_handler(instance, filename: str) -> str:
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"journal_image/{file_name}{file_suffix}"


class Task(RulesModel):
    class Statuses(models.IntegerChoices):
        OVERDUE = 10, _("Overdue")
        DUE = 20, _("Due")
        PENDING = 30, _("Pending")
        INACTIVE = 40, _("Inactive")

    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    object = models.ForeignKey(
        Object,
        verbose_name=_("object"),
        related_name="task_object",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        _("status"), choices=Statuses.choices, default=Statuses.PENDING
    )
    due_at = models.DateTimeField(_("due at"), blank=True, null=True)
    overdue_at = models.DateTimeField(_("overdue at"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ["status", "overdue_at", "due_at", "updated_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/task/{self.id}"

    def get_new_task_status(self) -> int:
        now = timezone.now()
        new_task_status = Task.Statuses.PENDING
        if self.overdue_at and now >= self.overdue_at:
            new_task_status = Task.Statuses.OVERDUE
        elif self.due_at and now >= self.due_at:
            new_task_status = Task.Statuses.DUE
        return new_task_status

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.OVERDUE:
            status_color = "red"
        elif self.status == self.Statuses.DUE:
            status_color = "amber"
        elif self.status == self.Statuses.INACTIVE:
            status_color = "grey"
        return status_color


class Journal(RulesModel):
    object = models.ForeignKey(
        Object,
        verbose_name=_("object"),
        related_name="journal_object",
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        verbose_name=_("task"),
        related_name="journal_task",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    notes = models.TextField(_("notes"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=journal_image_upload_handler, blank=True, null=True
    )
    labor_costs = models.DecimalField(
        _("labor costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    material_costs = models.DecimalField(
        _("material costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self) -> str:
        return self.created_at + " @" + self.object

    def get_absolute_url(self) -> str:
        return f"/journal/{self.id}"


class Trigger(RulesModel):
    class Conditions(models.TextChoices):
        EQUALS = "==", _("equals")
        NOTEQUALS = "!=", _("not equals")
        LESSTHAN = "<", _("less than")
        LESSTHANOREQUALTO = "<=", _("less than or equal to")
        GREATERTHAN = ">", _("greater than")
        GREATERTHANOREQUALTO = ">=", _("greater than or equal to")

    class Actions(models.TextChoices):
        SENSORSTATUS10 = "sensor10", _("Set sensor status to green")
        SENSORSTATUS20 = "sensor20", _("Set sensor status to amber")
        SENSORSTATUS30 = "sensor30", _("Set sensor status to red")

    name = models.CharField(_("name"), max_length=200)
    sensor = models.ForeignKey(
        Sensor,
        verbose_name=_("sensor"),
        related_name="trigger_sensor",
        on_delete=models.CASCADE,
    )
    jsonpath_expression = models.CharField(_("JSONpath expression"), max_length=200)
    condition = models.CharField(
        _("condition"), max_length=2, choices=Conditions.choices
    )
    value = models.CharField(_("value"), max_length=200)
    action = models.CharField(
        _("action"),
        max_length=9,
        choices=Actions.choices,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self) -> str:
        return self.created_at + " @" + self.sensor

    def get_absolute_url(self) -> str:
        return f"/trigger/{self.id}"
