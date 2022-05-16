from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from maintenance.models import Task
from django.urls import reverse


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
        text_content = "***********\nTask status\n***********\n\n"

        text_content += self.get_overdue_tasks_content(user, groups_as_list)
        text_content += self.get_due_tasks_content(user, groups_as_list)

        text_content += "\n\nObjector"

        send_mail(
            subject,
            text_content,
            from_email,
            [to],
            fail_silently=False,
        )

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
            content = "\nOverdue tasks\n#############\n\n"

        for task in overdue_tasks_queryset:
            content += f":Task: {task.name}, https://objector.app{reverse('maintenance:task-detail', args=[task.pk, ])}\n"
            content += f":Object: {task.object}, https://objector.app{reverse('inventory:object-detail', args=[task.object.pk, ])}\n"
            content += f":Due at: {task.due_at}\n"
            content += f":Overdue at: {task.overdue_at}\n"
            content += "-- \n"

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
            content = "\nDue tasks\n#########\n\n"

        for task in due_tasks_queryset:
            content += f":Task: {task.name}, https://objector.app{reverse('maintenance:task-detail', args=[task.pk, ])}\n"
            content += f":Object: {task.object}, https://objector.app{reverse('inventory:object-detail', args=[task.object.pk, ])}\n"
            content += f":Due at: {task.due_at}\n"
            content += f":Overdue at: {task.overdue_at}\n"
            content += "-- \n"

        return content
