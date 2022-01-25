from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import PermissionRequiredMixin
from .models import Location, Object
from maintenance.models import Task, Journal
from .forms import ObjectForm


class ObjectListView(LoginRequiredMixin, ListView):
    model = Object
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        qs = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_team__in=groups_as_list)
            | Object.objects.filter(maintenance_team__in=groups_as_list)
        )
        return qs


class ObjectCreateView(LoginRequiredMixin, CreateView):
    model = Object
    form_class = ObjectForm

    def get_initial(self):
        initial = {}
        initial["owner"] = self.request.user.id
        try:
            initial["location"] = int(self.request.GET["location"])
        except:
            pass

        try:
            initial["management_team"] = int(self.request.GET["management_team"])
        except:
            pass

        try:
            initial["maintenance_team"] = int(self.request.GET["maintenance_team"])
        except:
            pass

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ObjectDetailView(PermissionRequiredMixin, DetailView):
    model = Object
    permission_required = "inventory.view_object"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = Task.objects.filter(object=self.object.id)
        context["journal"] = Journal.objects.filter(object=self.object.id)
        return context


class ObjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Object
    permission_required = "inventory.change_object"
    raise_exception = True
    form_class = ObjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ObjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Object
    permission_required = "inventory.delete_object"
    raise_exception = True
    success_url = reverse_lazy("inventory:object-list")


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    permission_required = "view_location"
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        qs = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_team__in=groups_as_list)
            | Location.objects.filter(maintenance_team__in=groups_as_list)
        )
        return qs


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = [
        "name",
        "description",
        "image",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_team",
        "maintenance_team",
    ]

    def get_initial(self):
        initial = {}
        initial["owner"] = self.request.user.id

        try:
            initial["management_team"] = int(self.request.GET["management_team"])
        except:
            pass

        try:
            initial["maintenance_team"] = int(self.request.GET["maintenance_team"])
        except:
            pass

        return initial


class LocationDetailView(PermissionRequiredMixin, DetailView):
    model = Location
    permission_required = "inventory.view_location"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = Object.objects.filter(location=self.object.id)
        return context


class LocationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Location
    permission_required = "inventory.change_location"
    raise_exception = True
    fields = [
        "name",
        "description",
        "image",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_team",
        "maintenance_team",
    ]


class LocationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Location
    permission_required = "inventory.delete_location"
    raise_exception = True
    success_url = reverse_lazy("inventory:location-list")
