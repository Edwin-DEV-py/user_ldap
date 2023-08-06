from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,redirect
from django.contrib import messages,auth

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password) #metodo de autenticacion
        auth.login(request, user)
        return redirect('index')
    return render(request,'login.html')

def index(request):
    return render(request,'index.html')