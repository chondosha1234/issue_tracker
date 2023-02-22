from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('create_account', views.CreateAccountView.as_view(), name='create_account'),
    path('logout', views.logout, name='logout'),
]
