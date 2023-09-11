from django import forms
from .models import HazardReport

class HazardReportForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    class Meta:
        model = HazardReport
        fields = ['category', 'description', 'photo']

        widgets = {
            "category": forms.Select(attrs={"class":"form-control"}),
        }