from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Team


class TeamMemberCreateForm(forms.ModelForm):
    email = forms.EmailField(label=_("email"))

    class Meta:
        model = Team
        fields = [
            "email",
        ]


class TeamMemberDeleteForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []
