from django import forms
from ..tasks.models import Tasks
from .models import Projects

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'priority', 'status', 'start', 'end', 'executor']

    start = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    end = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))

class Project_create_form(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
            'name',
            'description',
            'start',
            'end',
            'status',
            'manager'
        ]
    start = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    end = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))