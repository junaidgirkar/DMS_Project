# forms.py

from django import forms

class PredictionForm(forms.Form):
    county = forms.CharField(label='County Name', max_length=100)
    years = forms.IntegerField(label='Forecast Years')
    amount = forms.DecimalField(label='Budget', max_digits=12, decimal_places=2)
