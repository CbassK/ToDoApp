from django import forms

# Reordering Task Position View

class PositionForm(forms.Form):
    position = forms.CharField()