from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.db.models import Min, Max
from inventory.models import Location
from maintenance.models import Task
import datetime


class HomeTemplateView(TemplateView):
    template_name = "common/home.html"


class LogoutRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs) -> str:
        django_logout(self.request)
        domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
        client_id = settings.SOCIAL_AUTH_AUTH0_KEY
        return_to = self.request.build_absolute_uri("/")
        return f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "common/dashboard.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        overdue_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.OVERDUE
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
        )
        due_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.DUE
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
        )
        pending_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.PENDING
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.PENDING,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.PENDING,
            )
        )
        location_queryset = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_group__in=groups_as_list)
            | Location.objects.filter(maintenance_group__in=groups_as_list)
        )
        context["overdue_tasks_count"] = overdue_tasks_queryset.count()
        context["due_tasks_count"] = due_tasks_queryset.count()
        context["pending_tasks_count"] = pending_tasks_queryset.count()
        context["locations"] = location_queryset
        context["locations_aggregates"] = location_queryset.aggregate(
            Min("latitude"), Max("latitude"), Min("longitude"), Max("longitude")
        )
        context["current_datetime"] = datetime.datetime.now()

        return context
