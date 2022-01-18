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
from .models import Work, Journal
from .forms import WorkForm


class WorkListView(LoginRequiredMixin, ListView):
    model = Work
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        qs = (
            Work.objects.filter(objekt__owner=self.request.user)
            | Work.objects.filter(objekt__management_team__in=groups_as_list)
            | Work.objects.filter(objekt__maintenance_team__in=groups_as_list)
        )
        return qs


class WorkCreateView(LoginRequiredMixin, CreateView):
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy("maintenance:work-list")

    def get_initial(self):
        initial = {}
        initial["owner"] = self.request.user.id
        try:
            initial["objekt"] = int(self.request.GET["objekt"])
        except:
            pass

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class WorkDetailView(PermissionRequiredMixin, DetailView):
    model = Work
    permission_required = "journal.view_work"
    raise_exception = True


class WorkUpdateView(PermissionRequiredMixin, UpdateView):
    model = Work
    permission_required = "journal.change_work"
    raise_exception = True
    form_class = WorkForm
    success_url = reverse_lazy("maintenance:work-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.status = Work.get_new_work_status(instance)
        instance.save()
        return super(WorkUpdateView, self).form_valid(form)


class WorkDeleteView(PermissionRequiredMixin, DeleteView):
    model = Work
    permission_required = "journal.delete_work"
    raise_exception = True
    success_url = reverse_lazy("maintenance:work-list")


class WorkJournalCreate(PermissionRequiredMixin, CreateView):
    pass
