from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField

from accounts.models import User
from accounts.models import Address


class DetailsAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('formatted_address','county','state','village','House_number','floor','unit','postal_code')
        widgets = {
            'formatted_address': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'county': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'state': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'House_number': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'floor': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'required ': 'true'})

        }
        # def clean_
class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('formatted_address','county','state','village','House_number','floor','unit','postal_code')
        widgets = {
            'formatted_address': forms.Textarea(attrs={'class': 'form-control','required ':'true'}),
            'county': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'state': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'House_number': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'floor': forms.TextInput(attrs={'class': 'form-control','required ':'true'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code':forms.TextInput(attrs={'class':'form-control','required ':'true'})
        }
class RegisterForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='گذرواژه', widget=forms.TextInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(label='تکرار گذرواژه', widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField(label='')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.object.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('لطفا شماره تلفن صحیح وارد نمایید')
        return phone_number

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password')
        password2 = cd.get('repassword')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('گذرواژه و تکرار آن را صحیح وارد نمایید')
        if len(password1) < 8:
            raise forms.ValidationError('گذرواژه ی شما کمتر از هشت کارکتر است')
        if not any(n.isalpha() for n in password1):
            raise forms.ValidationError('گذرواژه ی شما باید شامل یک حرف کوچک باشد')
        if not any(n.isupper() for n in password1):
            raise forms.ValidationError('گذرواژه ی شما باید شامل یک حرف بزرگ باشد')
class VerifyForm(forms.Form):
    code_Rand = forms.CharField(label='کد تایید را وارد کنید', widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    phone_number = forms.CharField(label='تلفن همراه', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='گذرواژه', widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField(label='')



class ChangeInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.TextInput(attrs={'class': 'form-control', 'data-jdp': 'True'})
        }

    def create(self, cd):
        return User.object.create(**cd)



class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'form-control'}))


class ChangePassword(forms.Form):
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('لطفا رمز عبور و گذرواژه ی صحیح وارد نمایید')
