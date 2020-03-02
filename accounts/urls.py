from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import CustomSignInView, CustomSignUpView, UserProfileView, UserProfileEditView

urlpatterns = [
    path('sign-in/', CustomSignInView.as_view(), name='sign_in'),
    path('sign-out/', LogoutView.as_view(), name='sign_out'),
    path('sign-up/', CustomSignUpView.as_view(), name='sign_up'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-edit/', UserProfileEditView.as_view(), name='profile_edit'),
]