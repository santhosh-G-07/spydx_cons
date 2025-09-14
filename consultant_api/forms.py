from django import forms
from django.contrib.auth.models import User
from .models import Consultant

from django import forms
from .models import ResumeUpload

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeUpload
        fields = ['file']
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
