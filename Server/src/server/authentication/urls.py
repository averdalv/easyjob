from django.urls import path

from authentication.views import *
app_name = 'authentication_app'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]