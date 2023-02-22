from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

from django.views.generic import View
from accounts.forms import LoginForm, CreateAccountForm

User = get_user_model()


def logout(request):
    auth_logout(request)
    return redirect('home')


class LoginView(View):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class CreateAccountView(View):
    template_name = "create_account.html"
    form_class = CreateAccountForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
        return redirect('accounts:create_account')
