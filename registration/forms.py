from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):

    name = forms.CharField(required=True)

    designation = forms.CharField(required=True)

    mobile = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "type": "tel",
            "placeholder": "Enter mobile number"
        })
    )

    class Meta:
        model = Registration
        fields = ["name", "designation", "mobile"]