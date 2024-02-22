# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import get_language, activate, gettext

from main.EmailBackEnd import EmailBackEnd

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
    finally:
        activate(cur_language)
    return cur_language

# Получаем выбранный язык
def get_lang(trans):
    if trans == 'en':
        lang = 'English'
    elif trans == 'ky':
        lang = 'Кыргызча'
    else:
        lang = 'Русский'
    return lang

def index(request):
    return render(request, 'index.html')


def loginPage(request):
    trans = translate(language='ru')
    actual_url = request.path.split('/')[2]

    return render(request, 'login.html', {'actual_url':actual_url})


def doLogin(request):
    if request.method != "POST":
        return redirect('login')
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_panel')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('client_home')
            else:
                messages.error(request, "Неверный логин!")
                return redirect('login')
        else:
            messages.error(request, "Неверный логин или пароль!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Пожалуйста для начала войдите в систему")



def logout_page(request):
    logout(request)
    return redirect('login')


# errors handler

def error_400(request, exception = None):
   context = {}
   response = render(request,'client_templates/pages/errors/400.html', context)
   response.status_code = 400
   return response

def error_403(request, exception = None):
   context = {}
   response = render(request,'client_templates/pages/errors/403.html', context)
   response.status_code = 403
   return response

def error_404(request, exception):
   context = {}
   response = render(request,'client_templates/pages/errors/404.html', context)
   
   response.status_code = 404
   return response


def error_500(request, exception = None):
   context = {}
   response = render(request,'client_templates/pages/errors/500.html', context)
   response.status_code = 500
   
   return response