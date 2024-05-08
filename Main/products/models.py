from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.urls import reverse

from utils.baseModel import BaseModel
from products.DiscountValidators import MaxDiscount, StockError, PriceError


class Product(BaseModel):
    STATUS = (
        ('None', 'none'),
        ('color', 'Color'),
        ('Size', 'size'),
        ('colorSize', 'ColorSize'),
        ('Weight', 'weight'),
    )

    name = models.CharField(max_length=100, verbose_name='نام محصول')
    sub_name = models.CharField(max_length=100, null=True, verbose_name='توضیحات کلی و کوتاه')
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=255, null=True)
    image = models.ImageField(upload_to='products/%Y/%M/%d', verbose_name='عکس اصلی')
    category = models.ForeignKey('Category', models.SET_NULL, 'categories_realted', null=True)
    category2 = models.ForeignKey('CategorySecond', models.SET_NULL, 'cat_2', null=True)
    category3 = models.ForeignKey('CategorySub', models.SET_NULL, 'category_subs', null=True)
    price = models.PositiveIntegerField(validators=[PriceError], default=0, verbose_name='قیمت')
    brand = models.ForeignKey('Brand', models.SET_NULL, 'brand_product_rel', null=True, verbose_name='برند محصول')
    is_available = models.BooleanField(default=True, verbose_name='موجود است یا خیر')
    desc = RichTextField(verbose_name='توضیحات')
    discount = models.PositiveIntegerField(validators=[MaxDiscount], default=0, verbose_name='تخفیف')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    total_sale = models.PositiveIntegerField(default=0, verbose_name='آمار کل خرید محصول')
    status = models.CharField(max_length=20, choices=STATUS, default='None')
    weight = models.PositiveIntegerField(default=0)
    # product_weight = models.ForeignKey('Weight',models.SET_NULL,'weight_product',null=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name}-{self.price}'

    @property
    def after_discount(self):
        unit_price = self.price
        if self.discount:
            unit_price = (100 - self.discount) * unit_price // 100
        return unit_price

    @property
    def countSeen(self):
        return self.seen_product.all().count()

    @property
    def profit_product(self):
        unit_price = self.price
        if self.discount:
            unit_price = unit_price * self.discount // 100
            return unit_price
        return False

    @property
    def get_absolute_url(self):
        return reverse('Products:ProductDetails', args=(self.id, self.slug))


# class ProductSpecifications(models.Model):
#     brand = models.ForeignKey('Brand',models.SET_NULL,'brand_product',null=True,blank=True)
#
class Color(BaseModel):
    COLOR_SELECT = (
        ('None', 'none'),
        ('red', 'red'),
        ('blue', 'blue'),
        ('yellow', 'yellow'),
        ('green', 'green'),
        ('black', 'black'),
        ('orange', 'orange'),
        ('white', 'white'),
    )
    name = models.CharField(max_length=20, choices=COLOR_SELECT, default='None')
    code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
class Size(BaseModel):
    SIZE_OPTION = (
        ('none', 'None'),
        ('XXSmall', 'XXSmall'),
        ('XSmall', 'XSmall'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XLarge', 'XLarge'),
        ('XXLarge', 'XXLarge'),
        ('XXXLarge', 'XXXLarge')

    )
    name = models.CharField(max_length=20, choices=SIZE_OPTION, default='Medium')

    def __str__(self):
        return self.name

# class SeenProduct(BaseModel):
#     ip = models.CharField(max_length=255)
#     product = models.ForeignKey('Product', models.CASCADE, 'seen_product')
#
#     def __str__(self):
#         return f'{self.ip} - {self.product}'

class extraImage(BaseModel):
    image = models.ImageField(verbose_name='')
    product = models.ForeignKey('Product', models.CASCADE, 'extra_image_product', verbose_name='')
class Brand(BaseModel):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='products/brand/%Y/%M/%d', null=True)

    def __str__(self):
        return self.name
class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class CategorySecond(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)
    is_available = models.BooleanField(default=True)
    Parent_Cat = models.ForeignKey('Category', models.CASCADE, 'parents_sub', null=True)

    def __str__(self):
        return self.name
class CategorySub(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)
    is_available = models.BooleanField(default=True)
    Parent_Cat = models.ForeignKey('Category', models.CASCADE, 'parent_sub_main')
    Parent_Cat_two = models.ForeignKey('CategorySecond', models.SET_NULL, 'parent_sub_two', null=True)

    def __str__(self):
        return self.name
class Weight(BaseModel):
    UNIT_SELECT = (
        ('None', 'هیچکدام'),
        ('gram', 'g'),
        ('kilogram', 'kg'),
    )
    Unit = models.CharField(max_length=40, choices=UNIT_SELECT, default='gram')
    from_number = models.PositiveIntegerField(default=0)
    to_number = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0, null=True)
    paking = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.from_number} {self.to_number} {self.Unit} '

    @property
    def Computing_Price(self):
        return self.price + self.paking

class VariantProduct(BaseModel):
    product = models.ForeignKey('Product', models.SET_NULL, 'var_product', null=True)
    size = models.ForeignKey('Size', models.SET_NULL, 'var_size', null=True, blank=True)
    price = models.PositiveIntegerField(default=0, validators=[PriceError])
    discount = models.PositiveIntegerField(default=0, validators=[MaxDiscount])
    stock = models.PositiveIntegerField(default=0, validators=[StockError])

    def __str__(self):
        return f' {self.product.name}'

    @property
    def after_discount(self):
        unit_price = self.price
        if self.discount:
            unit_price = (100 - self.discount) * unit_price // 100
        return unit_price

    @property
    def profit_product(self):
        unit_price = self.price
        if self.discount:
            unit_price = unit_price * self.discount // 100
            return unit_price
        return False

    @property
    def get_absolute_url(self):
        return reverse('Products:ProductDetails', args=(self.id, self.slug))




class Comment(BaseModel):
    user = models.ForeignKey('accounts.User', models.SET_NULL, 'userComment', null=True)
    product = models.ForeignKey('Product', models.CASCADE, 'ProductComment')
    is_replay = models.BooleanField(default=False)
    replay_to = models.ForeignKey('self', models.CASCADE, 'replay_comment', null=True, blank=True)
    body = RichTextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.phone_number}-{self.product.name}'


class Like(BaseModel):
    user = models.ForeignKey('accounts.User', models.CASCADE, 'user_like')
    product = models.ForeignKey('Product', models.SET_NULL, 'product_like', null=True)
    var_product = models.ForeignKey('VariantProduct',models.SET_NULL,'var_product_like',null=True)


# class VariantColor(BaseModel):
#     color = models.ForeignKey('Color', models.SET_NULL, 'var_color', null=True, blank=True)
#     price = models.PositiveIntegerField(default=0, validators=[PriceError])
#     discount = models.PositiveIntegerField(default=0, validators=[MaxDiscount])
#     stock = models.PositiveIntegerField(default=0, validators=[StockError])
#
#     def __str__(self):
#         return f' {self.color}'
#
#     @property
#     def final_price(self):
#         price = self.price
#         if self.discount:
#             price = (100 - self.discount) * price // 100
#         return price


# class VariantSize(BaseModel):
#     size = models.ForeignKey('Size', models.SET_NULL, 'var_size', null=True, blank=True)
#     price = models.PositiveIntegerField(default=0, validators=[PriceError])
#     discount = models.PositiveIntegerField(default=0, validators=[MaxDiscount])
#     stock = models.PositiveIntegerField(default=0, validators=[StockError])
#
#     def __str__(self):
#         return f' {self.size}'
#
#     @property
#     def final_price(self):
#         price = self.price
#         if self.discount:
#             price = (100 - self.discount) * price // 100
#         return price


class NewProduct(BaseModel):
    product = models.ForeignKey('Product', models.CASCADE, 'pro_new')

    def __str__(self):
        return self.product.name
