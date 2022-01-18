from django import forms
from .models import Team


class TeamMemberCreateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Team
        fields = [
            "email",
        ]


class TeamMemberDeleteForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []
