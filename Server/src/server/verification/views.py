from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import View
# Create your views here.
from authentication.models import User
from verification.token_generator import account_activation_token


class ConfirmEmailView(View):
    def get(self,request,uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.profile.set_email_verified()
            user.save()
            return HttpResponse('Ваша почта успешно активирована!')
        else:
            return HttpResponse('Неверная ссылка активации!')