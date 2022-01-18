from django.db import models
from rules.contrib.models import RulesModel
from django.utils import timezone
from inventory.models import Object
import uuid
import pathlib


def log_image_upload_handler(instance, filename):
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"objekt_image/{file_name}{file_suffix}"


class Work(RulesModel):
    class Statuses(models.IntegerChoices):
        OVERDUE = 10, "Overdue"
        DUE = 20, "Due"
        PENDING = 30, "Pending"
        INACTIVE = 40, "Inactive"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    object = models.ForeignKey(
        Object, related_name="work_objekt", on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        choices=Statuses.choices, default=Statuses.PENDING
    )
    due_at = models.DateTimeField(blank=True, null=True)
    overdue_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "overdue_at", "due_at", "updated_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/work/{self.id}"

    def get_new_work_status(self):
        now = timezone.now()
        new_work_status = Work.Statuses.PENDING
        if self.overdue_at and now >= self.overdue_at:
            new_work_status = Work.Statuses.OVERDUE
        elif self.due_at and now >= self.due_at:
            new_work_status = Work.Statuses.DUE
        return new_work_status

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
    work = models.ForeignKey(
        Work, related_name="work_journal", on_delete=models.RESTRICT
    )
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to=log_image_upload_handler, blank=True, null=True)
    labor_costs = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=9
    )
    material_costs = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=9
    )
    created_at = models.DateTimeField(auto_now_add=True)
