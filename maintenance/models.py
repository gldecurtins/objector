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

    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    object = models.ForeignKey(
        Object,
        verbose_name=_("Object"),
        related_name="task_object",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.PENDING
    )
    due_at = models.DateTimeField(_("Due at"), blank=True, null=True)
    overdue_at = models.DateTimeField(_("Overdue at"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
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
        verbose_name=_("Object"),
        related_name="journal_object",
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        verbose_name=_("Task"),
        related_name="journal_task",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    notes = models.TextField(_("Notes"), blank=True)
    image = models.ImageField(
        _("Image"), upload_to=journal_image_upload_handler, blank=True, null=True
    )
    labor_costs = models.DecimalField(
        _("Labor costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    material_costs = models.DecimalField(
        _("Material costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

    def get_absolute_url(self) -> str:
        return f"/journal/{self.id}"

    class Meta:
        ordering = ("-updated_at",)


class Trigger(RulesModel):
    class Conditions(models.TextChoices):
        EQUALS = "==", _("equals")
        NOTEQUALS = "!=", _("not equals")
        LESSTHAN = "<", _("less than")
        LESSTHANOREQUALTO = "<=", _("less than or equal to")
        GREATERTHAN = ">", _("greater than")
        GREATERTHANOREQUALTO = ">=", _("greater than or equal to")

    class Statuses(models.IntegerChoices):
        RED = 10, _("Alert")
        AMBER = 20, _("Warning")
        GREEN = 30, _("Normal")

    name = models.CharField(_("name"), max_length=200)
    sensor = models.ForeignKey(
        Sensor,
        verbose_name=_("Sensor"),
        related_name="trigger_sensor",
        on_delete=models.CASCADE,
    )
    jsonpath_expression = models.CharField(_("JSONPath expression"), max_length=200)
    condition = models.CharField(
        _("Condition"), max_length=2, choices=Conditions.choices
    )
    sensor_value = models.CharField(
        _("Sensor value"), max_length=200, blank=True, null=True
    )
    amber_value = models.CharField(
        _("Warning value"), max_length=200, blank=True, null=True
    )
    red_value = models.CharField(
        _("Alert value"), max_length=200, blank=True, null=True
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/trigger/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == Trigger.Statuses.RED:
            status_color = "red"
        elif self.status == Trigger.Statuses.AMBER:
            status_color = "amber"
        return status_color
