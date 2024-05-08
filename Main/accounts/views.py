from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.serializers import serialize
from random import randint
import jdatetime
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import RegisterForm, LoginForm, VerifyForm, ChangePassword, ChangeInfoForm, PhoneNumberForm, \
    DetailsAddressForm, AddressEditForm
from accounts.models import Otp, User, OtpChecked, Address
from products.models import Comment
from cart.cart import Cart, VariantCart
from products.Compare import Compare
from products.models import Like
from order.models import Order, OrderItem
from utils import sms, map_api


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'accounts/Register.html'

    # def setup(self, request, *args, **kwargs):
    #     self.next = 'accounts/login'
    #     return super().setup(request,*args, **kwargs)

    def get(self, request):
        ctx = {
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if otps := Otp.objects.filter(phone_number=cd.get('phone_number')):
                otps.delete()
            Random_Code = randint(100000, 999999)
            Otp.objects.create(phone_number=cd.get('phone_number'), Random_code=Random_Code)
            sms.send_code(cd.get('phone_number'), Random_Code)
            request.session['user_info'] = {
                'phone_number': cd.get('phone_number'),
                'password': cd.get('password1'),
                # 'next': self.next
            }
            # phone = request.session['user_info']['phone_number']
            return redirect('Accounts:VerifyRegister', )

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class RegisterVerifyView(View):
    template_name = 'accounts/RegisterVerify.html'
    form_class = VerifyForm

    def get(self, request):
        ctx = {
            'phone': request.session['user_info']['phone_number'],
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        user_info = request.session.get('user_info')
        otp_instance = Otp.objects.filter(phone_number=user_info.get('phone_number')).first()
        form = self.form_class(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code_Rand']
            if user_code != otp_instance.Random_code:
                otp_instance.delete()
                del request.session['user_info']
                return redirect('Accounts:Register')

            otp_exp = otp_instance.created + jdatetime.timedelta(minutes=2)
            now = jdatetime.datetime.now()
            if otp_exp < now:
                otp_instance.delete()
                del request.session['user_info']
                return redirect('Accounts:Register')
            user = User.object.create_user(phone_number=user_info.get('phone_number'),
                                           password=user_info.get('password'))
            # if next_param := user_info.get('next'):
            #     otp_instance.delete()
            #     del request.session['user_info']
            #     return redirect(next_param)

            otp_instance.delete()
            del request.session['user_info']
            login(request, user)
            return redirect('Home:home')

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        ctx = {
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        next_param = request.GET.get('next')
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            passw = form.cleaned_data['password']
            if user := authenticate(request, phone_number=phone, password=passw):
                login(request, user)
                if next_param:
                    print(next_param)
                    return redirect(next_param)
                else:
                    return redirect('Home:home')
            return redirect('Accounts:Register')
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class logOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('Home:home')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/Profile.html'
    form_class = ChangeInfoForm
    DetailsAddressForm = DetailsAddressForm
    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        if lat or lng:
            lat = float(lat)
            lng = float(lng)
            if location_user := map_api.map(lat, lng):
                request.session['user_address'] = {
                    'formatted_address': location_user["formatted_address"],
                    'county': location_user["county"],
                    'state': location_user['state'],
                    "village": location_user['village'],
                }

                comments = Comment.objects.filter(Q(user=request.user), Q(active=False))
                ctx = {
                    'compare': Compare(request),
                    'order_history': Order.objects.filter(user=request.user, paid=True),
                    'form_information': self.form_class(instance=request.user),
                    'cart': Cart(request),
                    'variant_cart': VariantCart(request),
                    'list': Like.objects.filter(user=request.user),
                    'location_user': location_user,
                    'comments': comments,
                    'accepted_comment': Comment.objects.filter(Q(user=request.user), Q(active=True)),
                }
                return render(request, self.template_name, ctx)

            return render(request, 'accounts/Profile.html', {'error': 'Unable to retrieve location information.'})
        comments = Comment.objects.filter(Q(user=request.user), Q(active=False))
        ctx = {
            'compare': Compare(request),
            'order_history': Order.objects.filter(user=request.user, paid=True),
            'form_information': self.form_class(instance=request.user),
            'cart': Cart(request),
            'variant_cart': VariantCart(request),
            'list': Like.objects.filter(user=request.user),
            'comments': comments,
            'accepted_comment': Comment.objects.filter(Q(user=request.user), Q(active=True)),
            'user_address': Address.objects.filter(user=request.user),
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ctx = {
                'compare': Compare(request),
                'order_history': Order.objects.filter(user=request.user, paid=True),
                'form_information': self.form_class(instance=request.user),
                'cart': Cart(request),
                'variant_cart': VariantCart(request),
                'list': Like.objects.filter(user=request.user),
                'accepted_comment': Comment.objects.filter(Q(user=request.user), Q(active=True)),
                'user_address': Address.objects.filter(user=request.user),
            }
            return render(request, self.template_name, ctx)

        ctx = {
            'form_information': form,
        }
        return render(request, self.template_name, ctx)


class SaveAddress(View):
    template_name = 'accounts/Profile.html'
    form_class = DetailsAddressForm

    def get(self, request):
        user_address = request.session.get('user_address')
        print(request.session.get('user_address'))
        if user_address:
            ctx = {
                'user_address': Address.objects.filter(user=request.user),
                'DetailsAddressForm': self.form_class(),
                'formatted_address': user_address.get("formatted_address"),
                'county': user_address.get("county"),
                'state': user_address.get('state'),
                'village': user_address.get('village')
            }
            return render(request, self.template_name, ctx)
        return redirect('Accounts:Profile')

    def post(self, request):
        address = Address.objects.all()
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not address.filter(user=request.user, formatted_address__exact=cd.get("formatted_address"),
                                  county__exact=cd.get("county"), state__exact=cd.get('state'),
                                  village__exact=cd.get('village')
                    , House_number__exact=cd.get('House_number'), floor__exact=cd.get('floor'),
                                  unit__exact=cd.get('unit')):
                ad = form.save(commit=False)
                ad.user = request.user
                ad.save()
            return redirect('Accounts:Profile')
        ctx = {
            'user_address': Address.objects.filter(user=request.user),
            'form': form
        }
        return render(request, self.template_name, ctx)


class editAddress(View):
    template_name = 'accounts/EditAddress.html'
    form_class = AddressEditForm

    def get(self, request, id_address):
        # if id_address:
        if address := get_object_or_404(Address, id=id_address, user=request.user):
            ctx = {
                'form': self.form_class(instance=address),
                'Address_user': Address.objects.filter(user=request.user)
            }
            return render(request, self.template_name, ctx)

    #     else:
    #         address = Address.objects.filter(user=request.user).first()
    #         ctx = {
    #             'form': self.form_class(instance=address),
    #             'Address_user': Address.objects.filter(user=request.user)
    #         }
    #         return render(request, self.template_name, ctx)
    # return redirect('Accounts:Profile')

    def post(self, request, id_address=None):
        if address := get_object_or_404(Address, id=id_address, user=request.user):
            form = self.form_class(request.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect('Accounts:Profile')
            ctx = {
                'address': address,
                'user_address': Address.objects.filter(user=request.user),
                'form': form,
            }
            return render(request, self.template_name, ctx)
    # return HttpResponseBadRequest("Invalid address ID")


class removeAddress(View):
    template_name = 'accounts/Profile.html'

    def get(self, request):
        if address := get_object_or_404(Address, id=request.GET.get('address_id'), user=request.user):
            # if request.GET.get('del'):
            #     print('hi')
            address.delete()
            return HttpResponse('success')
        # else:
        #     address.delete()
        #     return HttpResponse('success')


class ForgetPasswordView(View):
    form_class = PhoneNumberForm
    template_name = 'accounts/ForgetPassword.html'

    def get(self, request):
        ctx = {
            'form': self.form_class
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if otps := Otp.objects.filter(phone_number=phone_number).first():
                otps.delete()
            Random_code = randint(100000, 999999)
            Otp.objects.create(phone_number=phone_number, Random_code=Random_code)
            sms.send_code(phone_number, Random_code)
            messages.add_message(request,200,f' کد شما{Random_code}','success')
            request.session['user_forget'] = {
                'phone_number': phone_number
            }
            return redirect('Accounts:ForgetVerify')

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class ForgetPasswordVerifyView(View):
    form_class = VerifyForm
    template_name = 'accounts/ForgetPasswordVerify.html'

    def get(self, request):
        ctx = {
            'phone': request.session['user_forget']['phone_number'],
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        user_forget = request.session.get('user_forget')
        otps = Otp.objects.filter(phone_number=user_forget.get('phone_number')).first()
        if form.is_valid():
            user_code = form.cleaned_data['code_Rand']
            if user_code != otps.Random_code:
                otp1 = OtpChecked.objects.create(Otp_code=user_code, phone_number=user_forget.get('phone_number'))
                otp1.block = True
                if OtpChecked.objects.filter(phone_number=user_forget.get('phone_number')).count() > 3:
                    ex = OtpChecked.objects.filter(phone_number=user_forget.get('phone_number')).last()
                    messages.add_message(request, 200,
                                         str(ex.created) + 'لطفا یک دقیقه بعد تلاش کنید، دسترسی شما محدود شد',
                                         'danger')
                    end_time = ex.created + jdatetime.timedelta(minutes=1)
                    now1 = jdatetime.datetime.now()
                    if end_time < now1:
                        OtpChecked.objects.filter(phone_number=user_forget.get('phone_number')).delete()
                    return redirect('Home:home')

                return redirect('Accounts:Forget')

            exp_date = otps.created + jdatetime.timedelta(minutes=2)
            now = jdatetime.datetime.now()
            if now > exp_date:
                otps.delete()
                del request.session['user_forget']
                return redirect('Accounts:ForgetVerify')
            # user =  User.object.filter(phone_number=user_forget.get('phone_number')).first()
            request.session['send_phone_number'] = {
                'phone_number': user_forget.get('phone_number')
            }

            return redirect('Accounts:PasswordChange')
        ctx = {

            'form': form
        }
        return render(request, self.template_name, ctx)


class ForgetPasswordChangeView(View):
    template_name = 'accounts/ForgetPasswordChange.html'
    form_class = ChangePassword

    def get(self, request):
        ctx = {
            # 'phone': request.session['send_phone_number']['phone_number'],
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user = User.object.filter(phone_number=request.session['send_phone_number']['phone_number']).first()
            user.set_password(password1)
            user.save()
            return redirect('Accounts:Login')

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)
