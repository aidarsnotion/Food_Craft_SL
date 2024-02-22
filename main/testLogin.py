from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import *

@csrf_exempt
def authorization(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    messages = ""

    try:
        account = authenticate(username=username, password=password)

        if account is not None and request.method == 'POST':
            login(request, account)
            messages = "Неверный логин или пароль!"
        else:
            messages = "Неверный логин или пароль!"
    except:
        if username == "":
            messages = "Неверный логин или пароль!"
        elif password == "":
            messages = "Неверный логин или пароль!"
        else:
            messages = "Неверный логин или пароль!"
    
    return messages
