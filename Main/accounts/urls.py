from django.urls import path
from accounts import views

app_name = 'Accounts'

urlpatterns = [
    path('Register/',views.RegisterView.as_view(),name='Register'),
    path('VerifyRegister/',views.RegisterVerifyView.as_view(),name='VerifyRegister'),
    path('Login/',views.LoginView.as_view(),name='Login'),
    path('Logout/',views.logOutView.as_view(),name='Logout'),

    path('Profile/',views.ProfileView.as_view(),name='Profile'),


    path('ForgetPassword/', views.ForgetPasswordView.as_view(), name='Forget'),
    path('ForgetPasswordVerify/', views.ForgetPasswordVerifyView.as_view(), name='ForgetVerify'),
    path('ForgetPasswordChange/', views.ForgetPasswordChangeView.as_view(), name='PasswordChange'),

    path('SaveAddress/',views.SaveAddress.as_view(),name='address'),
    path('DeleteAddress/', views.removeAddress.as_view(), name='DeleteAddress'),

    # path('EditAddress/', views.editAddress.as_view(), name='editAddressDel'),
    path('EditAddress/<int:id_address>/', views.editAddress.as_view(), name='editAddress'),

]