from django import forms
from .models import Location, Object


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = [
            "name",
            "description",
            "image",
            "location",
            "owner",
            "management_team",
            "maintenance_team",
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        location_queryset = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_team__in=groups_as_list)
            | Location.objects.filter(maintenance_team__in=groups_as_list)
        )

        self.fields["location"].queryset = location_queryset
