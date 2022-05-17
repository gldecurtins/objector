from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from maintenance.models import Task
from django.utils import translation, timezone, formats
import markdown


class Command(BaseCommand):
    help = "Sends task status mail"

    def handle(self, *args, **options) -> None:
        self.get_users()

    def get_users(self) -> None:
        User = get_user_model()
        users = User.objects.filter(email__isnull=False)
        for user in users:
            groups = user.groups.values_list("pk", flat=True)
            groups_as_list = list(groups)
            self.send_task_status_summary(user, groups_as_list)

    def send_task_status_summary(self, user, groups_as_list) -> None:
        translation.activate("de")
        subject, from_email, to = (
            _("Status report") + " " + formats.localize(timezone.localtime()),
            "info@objector.app",
            user.email,
        )

        overdue_tasks = self.get_overdue_tasks(user, groups_as_list)
        due_tasks = self.get_due_tasks(user, groups_as_list)

        text_content = f"# {_('Tasks')}\n"
        text_content += f"{_('Overdue')}: {overdue_tasks.get('count', 0)}, {_('Due')}: {due_tasks.get('count', 0)}\n\n"
        text_content += overdue_tasks.get("content", "")
        text_content += due_tasks.get("content", "")

        text_content += "\n\n[Objector](https://objector.app)"
        html_content = markdown.markdown(text_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_overdue_tasks(self, user, groups_as_list) -> dict:
        overdue_tasks = {}
        overdue_tasks["content"] = ""
        overdue_tasks["count"] = 0
        overdue_tasks_queryset = (
            Task.objects.filter(object__owner=user, status=Task.Statuses.OVERDUE)
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
        )
        if overdue_tasks_queryset:
            overdue_tasks["content"] = f"\n## {_('Overdue')}\n\n"
            for task in overdue_tasks_queryset:
                overdue_tasks["content"] += self.compile_task_content(task)
                overdue_tasks["count"] += 1

        return overdue_tasks

    def get_due_tasks(self, user, groups_as_list) -> dict:
        due_tasks = {}
        due_tasks["content"] = ""
        due_tasks["count"] = 0
        due_tasks_queryset = (
            Task.objects.filter(object__owner=user, status=Task.Statuses.DUE)
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
        )
        if due_tasks_queryset:
            due_tasks["content"] = f"\n## {_('Due')}\n\n"
            for task in due_tasks_queryset:
                due_tasks["content"] += self.compile_task_content(task)
                due_tasks["count"] += 1

        return due_tasks

    def compile_task_content(self, task) -> str:
        content = ""
        content += (
            f"+ {_('Task')}: [{task.name}](https://objector.app/task/{task.pk}/)\n"
        )
        content += (
            f"+ {_('Object')}: "
            f"[{task.object}](https://objector.app/object/{task.object.pk}/)\n"
        )
        if task.object.location:
            content += (
                f"+ {_('Location')}: "
                f"[{task.object.location}](https://objector.app/location/{task.object.location.pk}/)\n"
            )
        content += f"+ {_('Due at')}: {formats.localize(task.due_at)}\n"
        content += f"+ {_('Overdue at')}: {formats.localize(task.overdue_at)}\n"
        content += "---\n"

        return content
