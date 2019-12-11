
from django.contrib import admin
from django.urls import path, include

from verification.views import *

app_name = 'verification_app'

urlpatterns = [
    path('confirm_email/<slug:uidb64>/<slug:token>', ConfirmEmailView.as_view(), name='confirm_email'),
]
