from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class PlotSalesFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=AdminDateWidget(attrs={'placeholder': 'Fecha inicio'})
    )
    end_date = forms.DateField(
        required=False,
        widget=AdminDateWidget(attrs={'placeholder': 'Fecha fin'})
    )

