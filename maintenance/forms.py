from django import forms
from .models import Work
from inventory.models import Objekt


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = [
            "name",
            "description",
            "objekt",
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        objekt_queryset = (
            Objekt.objects.filter(owner=self.request.user)
            | Objekt.objects.filter(management_team__in=groups_as_list)
            | Objekt.objects.filter(maintenance_team__in=groups_as_list)
        )

        self.fields["objekt"] = forms.ModelChoiceField(queryset=objekt_queryset)
