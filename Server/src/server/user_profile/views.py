from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.views.generic.base import View

from location.models import City
from performer.models import PerformingSubCategory
from user_profile.forms import BasicSettingsFormPrivatePerson, BasicSettingsPerformerForm, ChangePasswordForm, \
    ChangeEmailAndPhoneForm, BasicSettingsFormFirm

from order.models import SimpleOrder, OrderStatus
from customer.models import Customer
from chat.models import Message
from order.services import get_orders

# TODO check only for authorized users
from verification.token_generator import account_activation_token


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.filter(message_to=request.user,is_read=False)
        if request.user.isCustomer:
            status = request.GET.get('status', None)
            if status:
                status = get_object_or_404(OrderStatus, value=status)
            customer = get_object_or_404(Customer, user=request.user)
            orders = get_orders(status=status, customer=customer, per_page=100) # tmp
        else:
            orders = get_orders(performer=request.user.performer)
        
        return render(request, 'user_profile/profile.html', {
            'orders': orders,
            'messages':messages
        })


class BasicSettingsView(LoginRequiredMixin, View):
    def make_context(self,request):
        user = request.user
        location = user.profile.location
        city = ""
        address = ""
        if location:
            city = location.city.value
            address = location.address
        data = {
            "about": user.profile.about,
            "birth_date": user.profile.birth_date,
            "phone_number": user.profile.phone_number,
            "gender": user.profile.gender,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "city": city,
            "location": address
        }
        if location:
            data['lat'] = location.lat
            data['lon'] = location.lon
        if user.isFirm:
            data["name"] = user.firm.name
            data["employee_number"] = user.firm.employee_number
            data["website"] = user.firm.website
            basic_settings_form = BasicSettingsFormFirm(data)
        else:
            data["birth_date"] = user.profile.birth_date
            data["gender"] = user.profile.gender
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            basic_settings_form = BasicSettingsFormPrivatePerson(data)
        context = {"base_settings_form": basic_settings_form}
        if user.isPerformer:
            performing_sub_categories = PerformingSubCategory.objects.filter(performer=user.performer)
            data_performer = {}
            for i, performing_sub_category in enumerate(performing_sub_categories):
                field_name_category = 'sub_category_%s' % (i,)
                field_name_price = 'price_%s' % (i,)
                field_name_negotiated = 'is_negotiated_%s' % (i,)
                field_name_hidden = "hidden_%s" % (i,)
                data_performer[field_name_category] = performing_sub_category.sub_category.value
                data_performer[field_name_negotiated] = performing_sub_category.is_price_negotiated
                if not performing_sub_category.is_price_negotiated:
                    data_performer[field_name_price] = performing_sub_category.price
                data_performer[field_name_hidden] = True
            languages = []
            for language in user.performer.languages.all():
                languages.append(language.value)
            data_performer["languages"] = languages
            if not user.isFirm:
                if user.performer.education:
                    data_performer["education_type"] = user.performer.education.education_type
                    data_performer[
                        "educational_institution_name"] = user.performer.education.educational_institution_name
            basic_settings_performer_form = BasicSettingsPerformerForm(data_performer)
            context["basic_settings_performer_form"] = basic_settings_performer_form
        return context
    def get(self, request):
        context = self.make_context(request)
        return render(request, 'user_profile/basic_settings.html', context)

    def post(self, request):
        user = request.user
        if user.isFirm:
            form = BasicSettingsFormFirm(request.POST)
        else:
            form = BasicSettingsFormPrivatePerson(request.POST)
        if form.is_valid():
            user = form.save(user)
            if request.FILES.__contains__("profile_picture"):
                user.profile.profile_picture = request.FILES["profile_picture"]
            user.save()
            context = self.make_context(request)
            context["is_settings_changed"] = True
            print(context)
            return render(request, 'user_profile/basic_settings.html', context)
        else:
            context = self.make_context(request)
            context['base_settings_form'] = form
            return render(request, 'user_profile/basic_settings.html', context)


class BasicSettingsPerformerView(LoginRequiredMixin, View):
    def post(self,request):
        if not request.user.isPerformer:
            return HttpResponseForbidden()
        form = BasicSettingsPerformerForm(request.POST)
        if form.is_valid():
            performer = request.user.performer
            form.save(performer)
        else:
            return HttpResponseBadRequest()
        basicSettings = BasicSettingsView()
        context = basicSettings.make_context(request)
        context["is_settings_changed"] = True
        return render(request, 'user_profile/basic_settings.html', context)
        # return HttpResponseRedirect(reverse('user_profile_app:profile'))


class PrivacySettingsView(LoginRequiredMixin, View):
    def get(self,request):
        change_password_form = ChangePasswordForm(request.user)
        data_email_and_phone = {"email":request.user.email,"phone_number":request.user.profile.phone_number}
        change_email_and_phone_form = ChangeEmailAndPhoneForm(data_email_and_phone)
        context = {"change_password_form":change_password_form,"change_email_and_phone_form":change_email_and_phone_form}
        return render(request,'user_profile/privacy_settings.html',context)
class ChangePasswordView(LoginRequiredMixin, View):
    def post(self,request):
        change_password_form = ChangePasswordForm(request.user,request.POST,instance=request.user)
        if change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)
        else:
            context = {"change_password_form": change_password_form}
            return render(request, 'user_profile/privacy_settings.html', context)
        # return HttpResponseRedirect(reverse('user_profile_app:profile'))
        change_password_form = ChangePasswordForm(request.user)
        data_email_and_phone = {"email": request.user.email, "phone_number": request.user.profile.phone_number}
        change_email_and_phone_form = ChangeEmailAndPhoneForm(data_email_and_phone)
        context = {"change_password_form": change_password_form,
                   "change_email_and_phone_form": change_email_and_phone_form,"is_password_changed":True}
        return render(request,'user_profile/privacy_settings.html',context)

class ChangeEmailAndPhoneView(LoginRequiredMixin,View):
    def post(self,request):
        change_email_and_phone_form = ChangeEmailAndPhoneForm(request.POST)
        if change_email_and_phone_form.is_valid():
            user = change_email_and_phone_form.save(request.user)
            update_session_auth_hash(request,user)
        else:
            return HttpResponseBadRequest(change_email_and_phone_form.errors)
        return HttpResponseRedirect(reverse('user_profile_app:profile'))

class ConfirmEmailView(LoginRequiredMixin,View):
    def get(self,request):
        current_site = get_current_site(request)
        email_subject = 'Подтвердите свою почту'
        message = render_to_string('user_profile/confirm_email.html', {
            'user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'token': account_activation_token.make_token(request.user),
        })
        to_email = request.user.email
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return HttpResponse('Мы отправили вам ссылку на почту, пожалуйста перейдите по ссылке чтобы подтвердить почту')

class UserBookmarks(LoginRequiredMixin, View):
    def get(self,request):
        return render(request, 'user_profile/bookmarks.html')