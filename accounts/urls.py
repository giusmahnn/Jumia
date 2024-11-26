from django.urls import path
from .views import *


urlpatterns = [
    path("google-signup/", GoogleAuthRedirect.as_view()),
    path("google/callback/", GoogleRedirect.as_view()),
    path("verify-email", VerifyEmail.as_view())
    
]