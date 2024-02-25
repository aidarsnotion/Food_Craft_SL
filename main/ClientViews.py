from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect, HttpResponse
import time
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from validate_email import validate_email
import smtplib
import json
from django.utils.translation import get_language, activate, gettext
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os

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

def client_home(request):
    return render(request, 'client_templates/index.html')

#Contact-us

def send_message(request):
    sucs=True
    if request.method == 'POST':
        
        settings.EMAIL_HOST_USER='csmbishkek@gmail.com'
        settings.EMAIL_HOST_PASSWORD='hswhmrcllyxoqbvx'

        Name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        to_email = 'csmbishkek@gmail.com'
        from_email =request.POST.get('email', '')
        phone = request.POST.get('phone')
        sub = request.POST.get('subject')
        subject = "Сообщение от пользователя, тема - " + sub 
        valid=validate_email(from_email, verify=True)

        if valid==True:
            
            try:
                body = {
                    'Name: ': "От кого: "+ Name, 
                    'from_email': "Эл.адрес: " + from_email,
                    'phone': "Тел:" + phone,
                    'text': "Сообщение: " + message,
                }
                messageAll = "\n".join(body.values())
                send_mail(subject, messageAll, from_email, [to_email],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Неправильный ввод данных')
            except smtplib.SMTPException:
                messages.add_message(request, messages.ERROR, 'Ошибка при отправлении, попробуйте еще раз!')
                return redirect ('contact')
            messages.add_message(request, messages.SUCCESS, 'Ваше сообщение отправлено!')
            return redirect ('contact')
        else:
            messages.add_message(request, messages.ERROR, 'Неправильный эл.адрес')
            
            return redirect ('contact')
    return redirect ('contact')


def about(request):
    actual_url = request.path.split('/')[2]

    context= {
        "actual_url":actual_url,
    }

    return render(request, 'client_templates/pages/about.html', context)

def contact(request):
    actual_url = request.path.split('/')[2]

    context= {
        "actual_url": actual_url,
    }

    return render(request, 'client_templates/pages/contact.html', context)

def cart(request):
    context= {

    }

    return render(request, 'client_templates/pages/pages/cart.html')

def product_details(request, id):
    actual_url = []
    actual_url.append(request.path.split('/')[2])
    actual_url.append(request.path.split('/')[3])
    result = "/".join(actual_url)
    product_id = Products.objects.get(id=id)
    fatacids = FatAcidCompositionOfMeal.objects.filter(product=id)
    mineracomp = MineralComposition.objects.get(product=id)
    amoinacids = AminoAcidComposition.objects.get(product=id)
    chemicals = Chemicals.objects.filter(product=id)
    if amoinacids.asparing == 0 and amoinacids.glutamin == 0 and amoinacids.serin == 0 and amoinacids.gistidin == 0 and amoinacids.glitsin == 0 and amoinacids.treonin == 0 and amoinacids.arginin == 0 and amoinacids.alanin == 0 and amoinacids.tirosin == 0 and amoinacids.tsistein == 0 and amoinacids.valin == 0 and amoinacids.metionin == 0 and amoinacids.triptofan == 0 and amoinacids.fenilalalin == 0 and amoinacids.izoleitsin == 0 and amoinacids.leitsin == 0 and amoinacids.lisin == 0 and amoinacids.prolin == 0:
        amoinacids = None
    all_zero = all(value.value == 0 for value in fatacids)

    if all_zero:
        fatacids = None
    context= {
        'product_id': product_id,
        'fatacids': fatacids,
        'mineracomp': mineracomp ,
        'amoinacids': amoinacids,
        'chemicals': chemicals,
        'actual_url':result,
    }
        
    return render(request, 'client_templates/pages/details.html',context)


def list(request):
    trans = translate(language='ru')
    actual_url = request.path.split('/')[2]
    list_of_products = Products.objects.filter(language = get_lang(trans=trans))
    
    context= {
        'list_of_products':list_of_products,
        'actual_url':actual_url,
    }

    return render(request, 'client_templates/pages/list.html', context)


def download_pdf(request):
    # Path to the PDF file
    pdf_path = 'C:/Users/Aigap/Desktop/permission/user_guide.pdf'

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="myfile.pdf"'
            return response
    else:
        return render(request, 'pdf_not_found.html')