from django.forms.models import ValidationError

def MaxDiscount(value):
    if value>100:
        raise ValidationError('لطفا تخفیف صحیح وارد نمایید')
    return value


def StockError(value):
    if not value:
        raise ValidationError('لطفا موجودی را وارد نمایید')
    return value


def PriceError(value):
    if value<10000:
        raise ValidationError('لطفا قیمت مناسب را وارد نمایید!')
    return value