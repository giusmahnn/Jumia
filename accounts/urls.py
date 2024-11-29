from django.urls import path
from .views import *


urlpatterns = [
    path("google-signup/", GoogleAuthRedirect.as_view()),
    path("google/callback/", GoogleRedirect.as_view()),
    path("verify-email", VerifyEmail.as_view()),
    path("signup/", CreateAccount.as_view()),
    path("login/", AccountLogin.as_view()),
    path("profile/", ProfileView.as_view()),
    path("reset-link/", ResetLinkView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("account-delete/", AccountDelete.as_view()),
    
]