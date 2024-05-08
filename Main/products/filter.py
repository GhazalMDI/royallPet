import django_filters
from django import forms

from products.models import Brand, Weight


class ProductFilter(django_filters.FilterSet):
    sort = (
        ('گران ترین', 'گران ترین',),
        ('ارزان ترین', 'ارزان ترین'),
        ('پربازدیدترین', 'پربازدیدترین'),
        ('پر فروش ترین', 'پر فروش ترین '),
        ('محصولات پرتخفیف', 'محصولات پرتخفیف'),
        ('جدیدترین ها', 'جدیدترین ها'),

    )
    less = django_filters.NumberFilter(field_name='price', label='از قیمت', lookup_expr='gte',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    more = django_filters.NumberFilter(field_name='price', label='تا قیمت', lookup_expr='lte',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    sort_product = django_filters.ChoiceFilter(choices=sort, label='مرتب سازی', method='get_sort',
                                               widget=forms.Select(attrs={'class': 'form-control'}))
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple())
    # weight = django_filters.ModelMultipleChoiceFilter(queryset=Weight.weight_product.all(),
    #                                                   widget=forms.CheckboxSelectMultiple())

    def get_sort(self, queryset, name, value):
        if value == 'ارزان ترین':
            o = 'price'
        if value == 'گران ترین':
            o = '-price'
        if value == 'محصولات پرتخفیف':
            o = '-discount'
        if value == 'پر فروش ترین':
            o = 'total_sale'
        if value == 'پربازدیدترین':
            o = 'countSeen'
        if value == 'جدیدترین ها':
            o = '-created'

        return queryset.order_by(o)
