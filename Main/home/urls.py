from django.urls import path
from home import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'Home'
urlpatterns = [
 path ('', views.homeView.as_view(),name='home'),
]