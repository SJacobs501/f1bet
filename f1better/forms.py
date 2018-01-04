from django import forms

class BetForm(forms.Form):
    money = forms.DecimalField(decimal_places=2)
