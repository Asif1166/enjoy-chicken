# Example DateRangeForm
from django import forms

from shop.models import CostSettings, ProductReview

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write Your Review', 'rows': 4}),
            'rating': forms.RadioSelect(choices=[
                (1, "⭐☆☆☆☆☆"),
                (2, "⭐⭐☆☆☆"),
                (3, "⭐⭐⭐☆☆"),
                (4, "⭐⭐⭐⭐☆"),
                (5, "⭐⭐⭐⭐⭐"),
            ]),
        }


class CostSettingsForm(forms.ModelForm):
    class Meta:
        model = CostSettings
        fields = ['shipping_cost']
        widgets = {
            'shipping_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }