from django import forms
from .models import Task, Journal
from inventory.models import Object


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "object",
            "due_at",
            "overdue_at",
            "status",
        ]
        widgets = {
            "due_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "placeholder": "Select a due date and time",
                },
            ),
            "overdue_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "placeholder": "Select an overdue date and time",
                },
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_team__in=groups_as_list)
            | Object.objects.filter(maintenance_team__in=groups_as_list)
        )

        self.fields["object"].queryset = object_queryset


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = [
            "object",
            "task",
            "notes",
            "image",
            "labor_costs",
            "material_costs",
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_team__in=groups_as_list)
            | Object.objects.filter(maintenance_team__in=groups_as_list)
        )
        task_queryset = (
            Task.objects.filter(object__owner=self.request.user)
            | Task.objects.filter(object__management_team__in=groups_as_list)
            | Task.objects.filter(object__maintenance_team__in=groups_as_list)
        )

        self.fields["object"].queryset = object_queryset
        self.fields["task"].queryset = task_queryset
