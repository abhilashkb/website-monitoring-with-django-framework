from django import forms
from .models import Domain

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name']