from django.shortcuts import render

# Create your views here.
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import View

from authentication.forms import RegistrationForm, RegistrationFormFirm
from performer.models import Performer
from customer.models import Customer
import logging

logger = logging.getLogger(__name__)


class RegistrationView(View):
    # def get(self, request):
    #     user_form = RegistrationForm()
    #     return render(request, 'authentication/registration.html',
    #                   {'form': user_form})

    def post(self, request):
        user_form = RegistrationForm(data=request.POST)
        account_type = request.POST['account_type']
        if account_type == 'pp':
            user_form = RegistrationForm(data=request.POST)
        elif account_type == 'firm':
            user_form = RegistrationFormFirm(data=request.POST)
        else:
            HttpResponse("Bad request")
        if user_form.is_valid():
            user = user_form.save()
            user.profile.profile_picture = "/profile_pictures/anonymous-user.png"
            user.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('user_profile_app:profile'))
        else:
            return render(request,'index.html',{"errors":user_form.errors,'form_error':'register'})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                logger.info("Successful login: %s", username)
                return HttpResponseRedirect(reverse('user_profile_app:profile'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            logger.error("Failed login: %s", username)
            return HttpResponse("Неправильные данные для входа")
    else:
        return HttpResponse("Bad request")


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
