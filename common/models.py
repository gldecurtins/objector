from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelMixin


class User(RulesModelMixin, AbstractUser):
    send_status_report_at = models.TimeField(
        _("send status report at"), blank=True, null=True
    )
    status_report_last_sent_at = models.DateTimeField(
        _("status report last sent at"), blank=True, null=True
    )

    def get_absolute_url(self) -> str:
        return f"/user/{self.id}"
