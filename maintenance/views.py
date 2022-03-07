from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import (
    PermissionRequiredMixin,
    permission_required,
    objectgetter,
)
from inventory.models import Sensor
from .models import Task, Journal, Trigger
from .forms import TaskForm, JournalForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        task_queryset = (
            Task.objects.filter(object__owner=self.request.user)
            | Task.objects.filter(object__management_team__in=groups_as_list)
            | Task.objects.filter(object__maintenance_team__in=groups_as_list)
        )
        return task_queryset


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = _("%(name)s was created successfully")

    def get_initial(self) -> dict:
        initial = {}
        initial["object"] = int(self.request.GET.get("object", False))
        return initial

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(PermissionRequiredMixin, DetailView):
    model = Task
    permission_required = "maintenance.view_task"
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["journal"] = Journal.objects.filter(task=self.object.id)
        return context


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    permission_required = "maintenance.change_task"
    raise_exception = True
    form_class = TaskForm

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form) -> dict:
        instance = form.save(commit=False)
        instance.status = Task.get_new_task_status(instance)
        instance.save()
        return super(TaskUpdateView, self).form_valid(form)


class TaskDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    permission_required = "maintenance.delete_task"
    raise_exception = True
    success_url = reverse_lazy("maintenance:task-list")


class JournalCreate(LoginRequiredMixin, CreateView):
    model = Journal
    form_class = JournalForm
    success_message = _("Journal entry created successfully")

    def get_initial(self) -> dict:
        initial = {}
        initial["object"] = int(self.request.GET.get("object", False))
        initial["task"] = int(self.request.GET.get("task", False))
        return initial

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class JournalDetailView(PermissionRequiredMixin, DetailView):
    model = Journal
    permission_required = "maintenance.view_journal"
    raise_exception = True


class JournalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Journal
    permission_required = "maintenance.change_journal"
    raise_exception = True
    form_class = JournalForm

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class JournalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Journal
    permission_required = "maintenance.delete_journal"
    raise_exception = True

    def get_success_url(self) -> str:
        object_id = self.object.object.id
        return reverse_lazy("inventory:object-detail", kwargs={"pk": object_id})


class TriggerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Trigger
    fields = ["name", "jsonpath_expression", "condition", "value", "action"]
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form):
        sensor = Sensor.objects.get(id=int(self.request.GET.get("sensor", False)))
        form.instance.sensor = sensor
        return super().form_valid(form)


class TriggerDetailView(PermissionRequiredMixin, DetailView):
    model = Trigger
    permission_required = "maintenance.view_trigger"
    raise_exception = True


class TriggerUpdateView(PermissionRequiredMixin, UpdateView):
    model = Trigger
    permission_required = "maintenance.change_trigger"
    raise_exception = True
    fields = ["name", "jsonpath_expression", "condition", "value", "action"]


class TriggerDeleteView(PermissionRequiredMixin, DeleteView):
    model = Trigger
    permission_required = "maintenance.delete_trigger"
    raise_exception = True

    def get_success_url(self) -> str:
        sensor_id = self.sensor.id
        return reverse_lazy("inventory:sensor-detail", kwargs={"pk": sensor_id})
