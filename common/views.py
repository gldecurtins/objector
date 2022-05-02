from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.models import Location
from django.views.generic import RedirectView


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
        location_queryset = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_group__in=groups_as_list)
            | Location.objects.filter(maintenance_group__in=groups_as_list)
        )
        context["locations"] = location_queryset
        return context
