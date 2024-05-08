from django import  forms

class locatForm(forms.Form):
    lat = forms.CharField()
    lng = forms.CharField()

class addressForm(forms.Form):
    location = forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))