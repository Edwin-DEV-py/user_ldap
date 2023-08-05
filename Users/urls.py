from django.contrib import admin
from django.urls import path
from .views import LDAPLogin

urlpatterns = [
    path('login',LDAPLogin.as_view())
]