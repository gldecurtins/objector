from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from maintenance.models import Task
import markdown


class Command(BaseCommand):
    help = "Sends task status mail"

    def handle(self, *args, **options):
        self.get_users()

    def get_users(self):
        User = get_user_model()
        users = User.objects.filter(email__isnull=False)
        for user in users:
            groups = user.groups.values_list("pk", flat=True)
            groups_as_list = list(groups)
            self.send_task_status_summary(user, groups_as_list)

    def send_task_status_summary(self, user, groups_as_list):
        subject, from_email, to = "Task status", "info@objector.app", user.email
        text_content = "# Task status\n\n"

        text_content += self.get_overdue_tasks_content(user, groups_as_list)
        text_content += self.get_due_tasks_content(user, groups_as_list)

        text_content += "\n\n[Objector](https://objector.app)"
        html_content = markdown.markdown(text_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_overdue_tasks_content(self, user, groups_as_list):
        content = ""
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
            content = "\n## Overdue tasks\n\n"

        for task in overdue_tasks_queryset:
            content += self.compile_task_content(task)

        return content

    def get_due_tasks_content(self, user, groups_as_list):
        content = ""
        due_tasks_queryset = (
            Task.objects.filter(object__owner=user, status=Task.Statuses.DUE)
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
        )
        if due_tasks_queryset:
            content = "\n## Due tasks\n\n"

        for task in due_tasks_queryset:
            content += self.compile_task_content(task)

        return content

    def compile_task_content(self, task):
        content = ""
        content += "+ Task: " f"[{task.name}](https://objector.app/task/{task.pk}/)\n"
        content += (
            "+ Object: "
            f"[{task.object}](https://objector.app/object/{task.object.pk}/)\n"
        )
        if task.object.location:
            content += (
                "+ Location: "
                f"[{task.object.location}](https://objector.app/location/{task.object.location.pk}/)\n"
            )
        content += f"+ Due at: {task.due_at}\n"
        content += f"+ Overdue at: {task.overdue_at}\n"
        content += "---\n"

        return content
