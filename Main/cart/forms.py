from django import forms

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,max_value=10,widget=forms.NumberInput(attrs={'class':'form-control inp'}))