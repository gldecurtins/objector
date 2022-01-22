from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel
from inventory.models import Object
import uuid
import pathlib


def log_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"object_image/{file_name}{file_suffix}"


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/object/{self.object.id}/task/{self.id}"

    def get_new_task_status(self):
        now = timezone.now()
        new_task_status = Task.Statuses.PENDING
        if self.overdue_at and now >= self.overdue_at:
            new_task_status = Task.Statuses.OVERDUE
        elif self.due_at and now >= self.due_at:
            new_task_status = Task.Statuses.DUE
        return new_task_status

    @property
    def get_status_color(self):
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
        _("image"), upload_to=log_image_upload_handler, blank=True, null=True
    )
    labor_costs = models.DecimalField(
        _("labor costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    material_costs = models.DecimalField(
        _("material costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return self.notes

    def get_absolute_url(self):
        return f"/object/{self.object.id}/journal/{self.id}"
