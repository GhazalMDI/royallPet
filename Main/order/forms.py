from django import forms

from accounts.models import User


class ReceiverInformationForm(forms.ModelForm):
    # address = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'hidden':'true'}))
    class Meta:
        model = User
        fields = ('phone_number','first_name','last_name')

        widgets = {
            'phone_number':forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def validate_unique(self):
        pass
class CouponForm(forms.Form):
    code = forms.CharField(max_length=255)