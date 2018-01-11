from django import forms

class AddDriverForm(forms.Form):
    first_name = forms.CharField(max_length=250, label = '', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name'
    }))

    last_name = forms.CharField(max_length=250, label = '', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name'
    }))

class AddTrackForm(forms.Form):
    name = forms.CharField(max_length=250, label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Track name'
     }))

    image = forms.CharField(max_length=1000, label='', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Image URL'
    }))