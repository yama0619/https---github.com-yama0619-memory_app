from django import forms
from .models import Memory
from django.forms.widgets import DateInput

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'description', 'created_at', 'photo', 'video', 'location']

    created_at = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'date-input'}),
    )