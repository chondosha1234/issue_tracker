from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('create_account', views.CreateAccountView.as_view(), name='create_account'),
    path('logout', views.logout, name='logout'),
    path('forgot-password', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete')
]
