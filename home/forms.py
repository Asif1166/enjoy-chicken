# forms.py

from django import forms
from .models import CV, Category

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['name', 'category', 'file']
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
    file = forms.FileField()
