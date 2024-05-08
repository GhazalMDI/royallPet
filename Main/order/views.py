from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
import jdatetime
from django.shortcuts import get_object_or_404
import uuid
from django.contrib.auth import login

from order.forms import ReceiverInformationForm, CouponForm
from cart.cart import Cart, VariantCart
from order.models import Order, OrderItem, Coupon
from products.models import Weight
from utils import pg, sms
from products.models import Product
from accounts.models import Address

PG_URL = 'https://panel.aqayepardakht.ir/startpay/sandbox'


class shopView(LoginRequiredMixin, View):
    form_class = ReceiverInformationForm
    form_coupon = CouponForm
    template_name = 'order/order.html'

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        ctx = {
            'address': address.first(),
            'all_address': address,
            'cart': Cart(request),
            'var_cart': VariantCart(request),
            'receiver_form': self.form_class(instance=request.user),
            'information_receiver': request.session.get('receiver_information'),
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        address = Address.objects.filter(user=request.user)
        selected_address_id = request.POST.get('selected_address_id')
        address_user = Address.objects.filter(id=selected_address_id).first()
        cart = Cart(request)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['receiver_information'] = {
                'l_name': cd.get('last_name'),
                'f_name': cd.get('first_name'),
                'address_id': address_user.id,
                'postal_code': address_user.postal_code,
                'phone_number': cd.get('phone_number')
            }
            ctx = {
                'address_user': address_user,
                'cart': cart,
                'var_cart': VariantCart(request),
                'information_receiver': request.session.get('receiver_information'),
                'receiver_form': form,
                'address': address.last(),
                'all_address': address,
            }

            return render(request, self.template_name, ctx)
        ctx = {
            'address_user': address_user,
            'cart': cart,
            'var_cart': VariantCart(request),
            'information_receiver': request.session.get('receiver_information'),
            'receiver_form': form,
            'address': address.last(),
            'all_address': address,
        }
        return render(request, self.template_name, ctx)


class SendView(LoginRequiredMixin, View):
    def post(self, request):
        session = request.session.get('receiver_information')
        if session:
            address = Address.objects.filter(id=session.get('address_id')).first()
            order = Order.objects.create(
                user=request.user,
                f_name=session.get('f_name'),
                l_name=session.get('l_name'),
                address=address,
                postal_code=session.get('postal_code'),
                phone_number=session.get('phone_number'),
            )
            del session
        else:
            address = Address.objects.filter(user=request.user).first()
            order = Order.objects.create(
                user=request.user,
                f_name=request.user.first_name,
                l_name=request.user.last_name,
                address=address,
                postal_code=address.postal_code,
                phone_number=request.user.phone_number,
            )
        for i in Cart(request):
            obj = OrderItem.objects.create(
                order=order,
                product_id=i['id'],
                price=i['after_discount'],
                quantity=i['quantity'],
            )
            obj.save()
        for v in VariantCart(request):
            obj = OrderItem.objects.create(
                order=order,
                variant_id=v['id'],
                price=v['after_discount'],
                quantity=v['quantity'],
            )
            obj.save()

        return redirect('order:OrderCreate', order.id)


class OrderCreateView(View, LoginRequiredMixin):
    template_name = 'order/OrderCreate.html'
    from_class = CouponForm

    def get(self, request, order_id):
        if order := Order.objects.filter(id=order_id).first():
            price = Weight.objects.filter(from_number__lt=order.sum_weight, to_number__gt=order.sum_weight).first()
            order.profit = Cart(request).get_total_profit + VariantCart(request).get_total_profit
            order.buy = order.get_total + price.Computing_Price
            order.save()
            ctx = {
                'price': price,
                'order': order,
            }
            return render(request, self.template_name, ctx)
        return redirect('order:OrderCreate')

    def post(self, request, order_id):
        form = self.from_class(request.POST)
        order = Order.objects.get(id=order_id)
        if form.is_valid():
            code = form.cleaned_data['code']
            now = jdatetime.datetime.now()
            if coupon := Coupon.objects.get(code__exact=code, active=True, from_date__lte=now, to_date__gte=now):
                order.discount = coupon.discount
                order.save()
                return redirect('order:OrderCreate', order.id)

            return redirect('order:OrderCreate', order.id)
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class StartPayView(View, LoginRequiredMixin):
    def get(self, request, order_id):
        if order := Order.objects.filter(id=order_id, paid=False).first():
            order.invoice_id = uuid.uuid4()
            order.save()
            data = {
                'amount': order.buy,
                'invoice_id': order.invoice_id
            }
            response = pg.create(data)
            res = response.json()
            if response.status_code == 200 and res.get('status') == 'success':
                return redirect(f'{PG_URL}/{res.get("transid")}')

            order.status = res.get('code')
            order.err = pg.get_error(res.get('code'))
            order.save()
            return redirect('Accounts:Profile')

        return render(request, '404.html')


class VerifyPay(View, LoginRequiredMixin):
    template_name = 'order/OrderVerify.html'

    def post(self, request):
        data = request.POST
        print(request.POST)
        if order := Order.objects.filter(invoice_id=data.get('invoice_id')).first():
            login(request, order.user)
            order.cardnumber = data.get('cardnumber')
            order.status = data.get('status')
            order.tracking_number = data.get('tracking_number')
            order.transid = data.get('transid')
            order.bank = data.get('bank')
            order.save()
            if data.get('status') == '1':
                data = {
                    'amount': order.buy,
                    'transid': order.transid
                }
                response = pg.Verify(data)
                res = response.json()
                if response.status_code == 200 and res.get('status') == 'success' and res.get('code') == '1':
                    order.paid = True
                    order.save()
                    items = order.order_item.all()

                    for i in items:
                        if i.product:
                            product = Product.objects.filter(id=i.product.id).first()
                            product.stock -= i.quantity
                            product.total_sale += i.quantity
                            if product.stock == 0:
                                product.is_available = False
                            product.save()

                    # sms.send_code()
                    # user = request.user
                    # if user:
                    #     request.user = user
                    #     login(request.user)
                    ctx = {
                        'order': order
                    }
                    return render(request, self.template_name, ctx)

                order.status = res.get('code')
                order.err = pg.get_error(res.get('code'))
                order.save()
                ctx = {
                    'order': order
                }
                return render(request, self.template_name, ctx)

            err = pg.get_error(data.get('status'))
            order.status = data.get('status')
            order.err = err
            order.save()

            ctx = {
                'order': order
            }

            return render(request, 'order/OrderVerify.html', ctx)

        return redirect('404.html')
