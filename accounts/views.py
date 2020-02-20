from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.urls import reverse

from accounts.forms import SignUpForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class CustomLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(request, messages.SUCCESS, "User created successfully")
        return render(request, 'sign_in.html')

    def post(self, request, *args, **kwargs):
        super(CustomLoginView, self).post(self,request, *args, **kwargs)

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(reverse('sign_in'))


class CustomSignUpView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'sign_up.html', {})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(**data)

            messages.add_message(request, messages.SUCCESS, "User created successfully")

            return HttpResponseRedirect(reverse('sign_in'))

        return HttpResponseRedirect(reverse('sign_up'))
