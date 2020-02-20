from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import CustomLoginView, CustomSignUpView

urlpatterns = [
    path('sign-in/', CustomLoginView.as_view(), name='sign_in'),
    path('sign-out/', LogoutView.as_view(), name='sign_out'),
    path('sign-up', CustomSignUpView.as_view(), name='sign_up')
]