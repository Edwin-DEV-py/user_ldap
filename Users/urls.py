from django.contrib import admin
from django.urls import path
from .api import *

urlpatterns = [
    path('login/', ldap_login, name='ldap-login'),
]