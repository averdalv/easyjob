
from django.contrib import admin
from django.urls import path, include

from user_profile.views import *

app_name = 'user_profile_app'

urlpatterns = [
    path('settings/basic', BasicSettingsView.as_view(), name='basic_settings'),
    path('settings/basic/performer',BasicSettingsPerformerView.as_view(),name='basic_settings_performer'),
    path('settings/privacy/', PrivacySettingsView.as_view(), name='privacy_settings'),
    path('settings/privacy/change_password', ChangePasswordView.as_view(), name='change_password'),
    path('settings/privacy/change_email_phone', ChangeEmailAndPhoneView.as_view(), name='change_email_and_phone'),
    path('settings/privacy/confirm_email',ConfirmEmailView.as_view(),name='confirm_email'),
    path('', ProfileView.as_view(), name="profile"),
    path('bookmarks', UserBookmarks.as_view(), name="bookmarks"),
]
