from django.db import models

from utils.baseModel import BaseModel
from accounts.models import User
from products.DiscountValidators import StockError, PriceError
from django_jalali.db import models as jmodels
from accounts.models import Address


class Order(BaseModel):
    user = models.ForeignKey('accounts.User', models.SET_NULL, 'user_order', null=True)
    f_name = models.CharField(max_length=255, null=True)
    l_name = models.CharField(max_length=255, null=True)
    address = models.ForeignKey('accounts.Address', models.SET_NULL, null=True, blank=True,
                                related_name='order_address')
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11, null=True)
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(default=0)
    buy = models.PositiveIntegerField(default=0, null=True)
    invoice_id = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    err = models.CharField(max_length=255, null=True)
    cardnumber = models.CharField(max_length=16, null=True)
    tracking_number = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    transid = models.CharField(max_length=255, null=True)
    profit = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f' {self.f_name} {self.l_name}'

    @property
    def get_total(self):
        total_price = sum(
            i.get_item_price for i in self.order_item.all()
        )
        if self.discount:
            return (100 - self.discount) * total_price // 100
        return total_price

    @property
    def sum_weight(self):
        return sum(
            i.weight_any for i in self.order_item.all()
        )


class OrderItem(BaseModel):
    product = models.ForeignKey('products.Product', models.SET_NULL, 'product_order_item', null=True)
    variant = models.ForeignKey('products.VariantProduct', models.SET_NULL, 'var_product_order_item', null=True)
    order = models.ForeignKey('Order', models.SET_NULL, 'order_item', null=True)
    price = models.PositiveIntegerField(default=0, validators=[PriceError])
    quantity = models.PositiveIntegerField(default=0, validators=[StockError])

    def __str__(self):
        product_name = self.product.name if self.product else 0
        variant_name = self.variant.product.name if self.variant and self.variant.product else 0
        return f'{product_name} {variant_name} {self.price} {self.quantity}'

    @property
    def get_item_price(self):
        return self.price * self.quantity

    @property
    def weight_any(self):
        w_product = self.product.weight * self.quantity if self.product else 0
        w_varProduct = self.variant.product.weight * self.quantity if self.variant and self.variant.product else 0
        return w_product + w_varProduct

    # @property
    # def weight_any(self):
    #     w_product = self.product.weight * self.quantity
    #     w_varProduct = self.variant.product.weight * self.quantity
    #     return w_product + w_varProduct


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    user = models.ManyToManyField('accounts.User', 'user_coupon', blank=True)
    discount = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=False)
    from_date = jmodels.jDateTimeField()
    to_date = jmodels.jDateTimeField()
