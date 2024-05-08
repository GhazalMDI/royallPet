from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from order import views
app_name = 'order'

urlpatterns = [
    path('shopping/',views.shopView.as_view(),name='shopping'),
    path('send/',views.SendView.as_view(),name='send'),
    path('OrderCreate/<int:order_id>/', views.OrderCreateView.as_view(), name='OrderCreate'),
    path('startpay/<int:order_id>/', views.StartPayView.as_view(), name='StartPay'),
    path('OrderVerify/', csrf_exempt(views.VerifyPay.as_view()), name='OrderVerify'),

]