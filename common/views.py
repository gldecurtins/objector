from django.contrib.auth import logout as django_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import PermissionRequiredMixin
from inventory.models import Location, Team
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
    FormView,
    RedirectView,
)
from django.urls import reverse_lazy
from .forms import TeamMemberCreateForm, TeamMemberDeleteForm


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
            | Location.objects.filter(management_team__in=groups_as_list)
            | Location.objects.filter(maintenance_team__in=groups_as_list)
        )
        context["locations"] = location_queryset
        return context


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    paginate_by = 10

    def get_queryset(self):
        qs = Team.objects.filter(owner=self.request.user)
        return qs


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = [
        "name",
        "description",
        "image",
        "owner",
    ]

    def get_initial(self) -> dict:
        return {"owner": self.request.user.id}


class TeamDetailView(PermissionRequiredMixin, DetailView):
    model = Team
    permission_required = "teamapp.view_team"
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(id=self.object.pk)
        context["members"] = group.user_set.all()
        return context


class TeamUpdateView(PermissionRequiredMixin, UpdateView):
    model = Team
    permission_required = "teamapp.change_team"
    raise_exception = True
    fields = ["name", "description", "image", "owner"]


class TeamDeleteView(PermissionRequiredMixin, DeleteView):
    model = Team
    permission_required = "teamapp.delete_team"
    raise_exception = True
    success_url = reverse_lazy("common:team-list")


class TeamMemberCreateView(PermissionRequiredMixin, FormView, DetailView):
    model = Team
    permission_required = "teamapp.change_team"
    template_name = "common/team_member_form.html"
    raise_exception = True
    form_class = TeamMemberCreateForm

    def get_success_url(self) -> str:
        return reverse_lazy("common:team-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        User = get_user_model()
        user = User.objects.get(email=form.data["email"])
        group = Group.objects.get(id=self.kwargs["pk"])
        group.user_set.add(user)
        return super(TeamMemberCreateView, self).form_valid(form)


class TeamMemberDeleteView(PermissionRequiredMixin, FormView, DetailView):
    model = Team
    permission_required = "teamapp.change_team"
    template_name = "common/team_member_confirm_delete.html"
    raise_exception = True
    form_class = TeamMemberDeleteForm

    def get_success_url(self) -> str:
        return reverse_lazy("common:team-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        group = Group.objects.get(id=self.kwargs["pk"])
        group.user_set.remove(self.kwargs["user_id"])
        return super(TeamMemberDeleteView, self).form_valid(form)
