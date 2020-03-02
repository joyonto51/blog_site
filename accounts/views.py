from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from django.urls import reverse

from accounts.models import User
from accounts.forms import SignUpForm, UserForm, UserInfoForm
from accounts.models import UserInfo
from blog_site import settings
from blog_site.views import BaseView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class CustomSignInView(LoginView):
    template_name = 'sign_in.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        # messages.add_message(request, messages.SUCCESS, "User created successfully")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        super(CustomSignInView, self).post(self, request, *args, **kwargs)

        next_url = kwargs.get('next', None)

        if request.user.is_authenticated and next_url:
            return HttpResponseRedirect(next_url)

        elif request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        elif not User.objects.filter(username=request.POST['username']).exists():
            messages.add_message(request, messages.ERROR, "User not found.")

        else:
            messages.add_message(request, messages.ERROR, "Password doesn't match.")

        return render(request, self.template_name, **kwargs)


class CustomSignUpView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'sign_up.html', {})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(**data)
            UserInfo.objects.create(user=user)

            messages.add_message(request, messages.SUCCESS, "Congrats, for sign up. Please use your mail as username to sign in.")

            return HttpResponseRedirect(reverse('sign_in'))

        return HttpResponseRedirect(reverse('sign_up'))


class UserProfileView(BaseView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self,request, *args, **kwargs):

        user_form = UserForm(request.POST, instance=request.user)
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=request.user.info)

        if user_form.is_valid() and user_info_form.is_valid():
            user_form.save()
            user_info_form.save()

            messages.add_message(request, messages.SUCCESS, "User info updated successfully")

        else:
            messages.add_message(request, messages.ERROR, "Form is not valid")

        return HttpResponseRedirect(reverse('profile'))


class UserProfileEditView(BaseView):
    template_name = 'profile_edit.html'

    def get(self, request, *args, **kwargs):

        context = {
            'profile': request.user.info,
        }

        return render(request, self.template_name, context)