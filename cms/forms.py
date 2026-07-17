from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name*'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email*'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject*'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write Message Here'}),
        }



class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y'],  # Accept both formats
        widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'})
    )
    
    class Meta:
        model = Reservation
        fields = ('name', 'email', 'phone', 'date', 'slot', 'total_person', 'status')
