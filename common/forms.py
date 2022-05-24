from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "send_status_report_at",
            "status_report_language",
        ]

    send_status_report_at = forms.TimeField(
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "placeholder": "Select a time",
            },
            format="%H:%M",
        ),
    )
