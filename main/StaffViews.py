from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from validate_email import validate_email
import smtplib
from django.http import HttpResponseBadRequest, JsonResponse
import json
import time
from django.db import IntegrityError
import numpy as np
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value, PULP_CBC_CMD, LpContinuous
from django.utils.translation import get_language, activate, gettext
from django.shortcuts import get_object_or_404
from scipy.optimize import linprog
from django.contrib.auth.decorators import login_required
from datetime import date
from collections import namedtuple
from django.db.models import Q
from main.Calculation_Recip import *

def staff_home(request):
    return render(request, 'client_templates/index.html')

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
    context= {

    }

    return render(request, 'client_templates/pages/about.html')

def contact(request):
    context= {

    }

    return render(request, 'client_templates/pages/contact.html')

def product_details(request, id):
        
    product_id = Products.objects.get(id=id)
    fatacids = FatAcidCompositionOfMeal.objects.filter(product=id)
    mineracomp = MineralComposition.objects.filter(product=id)
    amoinacids = AminoAcidComposition.objects.filter(product=id)
    chemicals = Chemicals.objects.filter(product=id)
    context= {
        'product_id': product_id,
        'fatacids': fatacids,
        'mineracomp': mineracomp ,
        'amoinacids': amoinacids,
        'chemicals': chemicals,
    }
        
    return render(request, 'client_templates/pages/details.html',context)


#Designing Recips
def meels(request):
    trans = translate(language='ru')
    actual_url = []
    actual_url.append(request.path.split('/')[2])
    actual_url.append(request.path.split('/')[3])
    result = "/".join(actual_url)

    product = Products.objects.all()
    etalon = Products.objects.filter(Category__Name_of_category = "Эталон")
    print(etalon)
    check = False
    region_choices = Regions.objects.filter(language=get_lang(trans))
    hide_ingredients = None

    context= {
        'ingredient': product,
        "hide_result" : check,
        "regions" : region_choices,
        "hide_ingredients" : hide_ingredients,
        "etalon": etalon,
        "actual_url": result,
    }

    return render(request, 'client_templates/pages/meels.html', context)

def get_recip_id(id):
    recip = Recips.objects.get(id=id)

    return recip

#Ajax Region
def load_courses(request):
    reg = request.GET.get('regionId')
    trans = translate(language='ru')
    ingredient = Products.objects.filter(Category__Region__id = reg, language = get_lang(trans))
    return render(request, 'client_templates/pages/dropdown_list_options.html', {'ingredients': ingredient})

@login_required
#Ajax calculations
def load_calculation(request):

    #Получаем название рецептуры
    recip_name = request.GET.get('Recip')
    #Получаем Регион продукта
    reg = json.loads(request.GET.get(('Regions')))
    #Получаем ID ингредиентов в виде списка
    ingredient = json.loads(request.GET.get('Ingredients'))
    #Получаем массовые доли ингредиентов в виде списка
    mass_fraction = json.loads(request.GET.get('MassFractions'))
    #Получаем цены ингредиентов в виде списка
    price = json.loads(request.GET.get('Prices'))
    #Получаем количество ингредиетов, целое число
    size = request.GET.get('counters')
    
    regions = Regions.objects.all()
    products = Products.objects.all()
    
    
    protein = 0.0
    fatacid = 0
    carbohydrates = 0
    total_mass_prot = 0

    error_message = "None"
    
    results = process_recipe(recip_name, reg, ingredient, mass_fraction, price, size)

    #Конвертируем значения в строку и записываем новые переменные, чтобы прочитать через Chart.js
    chart_protein = str(results.protein)
    chart_fatacid = str(results.fatacid)
    chart_carbo = str(results.carbohydrates)
    recip_name = str(recip_name)

    chart_kras = str(results.kras)
    chart_bc = str(results.bc)
    chart_U = str(results.U)
    chart_G = str(results.G)
    
    context = {
        'ingredients': products,
        'region' : regions,
        'error_message' : error_message,
        'chemicals' : results,
        'protein':chart_protein,
        'fatacid':chart_fatacid,
        'carbo':chart_carbo,
        'kras':chart_kras,
        'bc':chart_bc,
        'U':chart_U,
        'G':chart_G,
        'Json_Indredients':results.ingredients,
        'mass_fractions':results.mass_fraction,
        'recip_name': results.recip_name,
        'counter':results.counter,
    }
   
    return render(request, 'client_templates/pages/load-calculation.html', context)

def save_view(request):
    user_id = request.user.id
    trans = translate(language='ru')
    try:
        staff_object = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist as e:
        error = "Пользователь не найден!"
        return JsonResponse({'success': False, 'error':error})
    if request.method == 'POST':
        data = json.loads(request.body)

        size = data.get('counter')
        ingredient = data.get('ingred')
        ingredient_list = json.loads(ingredient)
        mass_fraction = data.get('mass_fraction')
        mass_fractions_list = json.loads(mass_fraction)
        table_chemicals = data.get('Table_Chemicals')
        table_chemicals_dict = json.loads(table_chemicals)[1]
        table_price = data.get('Table_Price')
        table_price_dict = json.loads(table_price)[1]

        if staff_object.user_type == "3": 
            table_scor = data.get('Table_Scor')
            table_scor_list = json.loads(table_scor)
        else:
            table_scor_list = []
        table_power = data.get('Table_Power')
        table_power_dict = json.loads(table_power)[1]
        if staff_object.user_type == "3": 
            table_kras = data.get('Table_Kras')
        recip_name = data.get('Recip')

        size = int(size)

        current_date = date.today()
        try:
            if not Recips.objects.filter(Q(name=recip_name) & Q(staff=user_id)).exists():
                recip_save = Recips(
                    name=recip_name,
                    cost_price_100gramm=float(table_price_dict['Table2_column0'].replace(',', '.')),
                    cost_price_1kg=float(table_price_dict['Table2_column1'].replace(',', '.')),
                    language=get_lang(trans=trans),
                    staff=staff_object,
                    date_analis=current_date
                )
                recip_save.save()
                recip_id = get_recip_id(recip_save.pk)
                if staff_object.user_type == "3": 
                    amino_recip = AminoAcidCompositionRecip(
                        recip=recip_id,
                        izoleitsin=float(table_scor_list[1]['Table3_column0'].replace(',', '.')),
                        leitsin=float(table_scor_list[1]['Table3_column1'].replace(',', '.')),
                        lisin=float(table_scor_list[1]['Table3_column2'].replace(',', '.')),
                        valin=float(table_scor_list[1]['Table3_column3'].replace(',', '.')),
                        metilcistein=float(table_scor_list[1]['Table3_column4'].replace(',', '.')),
                        feniltirosin=float(table_scor_list[1]['Table3_column5'].replace(',', '.')),
                        triptofan=float(table_scor_list[1]['Table3_column6'].replace(',', '.')),
                        treon=float(table_scor_list[1]['Table3_column7'].replace(',', '.')),
                        izoleitsin1=float(table_scor_list[2]['Table3_column0'].replace(',', '.')),
                        leitsin1=float(table_scor_list[2]['Table3_column1'].replace(',', '.')),
                        lisin1=float(table_scor_list[2]['Table3_column2'].replace(',', '.')),
                        valin1=float(table_scor_list[2]['Table3_column3'].replace(',', '.')),
                        metilcistein1=float(table_scor_list[2]['Table3_column4'].replace(',', '.')),
                        feniltirosin1=float(table_scor_list[2]['Table3_column5'].replace(',', '.')),
                        triptofan1=float(table_scor_list[2]['Table3_column6'].replace(',', '.')),
                        treon1=float(table_scor_list[2]['Table3_column7'].replace(',', '.')),
                        izoleitsin_a=float(table_scor_list[3]['Table3_column0'].replace(',', '.')),
                        leitsin_a=float(table_scor_list[3]['Table3_column1'].replace(',', '.')),
                        lisin_a=float(table_scor_list[3]['Table3_column2'].replace(',', '.')),
                        valin_a=float(table_scor_list[3]['Table3_column3'].replace(',', '.')),
                        metilcistein_a=float(table_scor_list[3]['Table3_column4'].replace(',', '.')),
                        feniltirosin_a=float(table_scor_list[3]['Table3_column5'].replace(',', '.')),
                        triptofan_a=float(table_scor_list[3]['Table3_column6'].replace(',', '.')),
                        treon_a=float(table_scor_list[3]['Table3_column7'].replace(',', '.')),
                        c_min=float(table_scor_list[4]['Table3_column0'].replace(',', '.'))
                    )
                    amino_recip.save()
                chemicals_recip = ChemicalsRecip(
                    recip=recip_id,
                    protein=float(table_chemicals_dict['Table1_column0'].replace(',', '.')),
                    fat=float(table_chemicals_dict['Table1_column1'].replace(',', '.')),
                    carbohydrates=float(table_chemicals_dict['Table1_column2'].replace(',', '.')),
                    kkal=float(table_power_dict['Table4_column0'].replace(',', '.')),
                    kJ=float(table_power_dict['Table4_column1'].replace(',', '.'))
                )
                chemicals_recip.save()
                saved_ingredients = []
                
                for i in range(0, int(size)):
                    ing = int(ingredient_list[i])
                    mf = float(mass_fractions_list[i].replace(',', '.'))
                    prod = Products.objects.get(id=ing)
                    ingredient_save = Ingredients(product=prod, mass_fraction=mf, recip=recip_id)
        
                    try:
                        ingredient_save.save()
                        saved_ingredients.append(ingredient_save)
                    except Exception as e:
                        print(f"Ошибка сохранения ингредиента: {e}")

            else:
                return JsonResponse({'success': False, 'error':"Рецепт с таким названием уже существует"})
        except Exception as e:
            return JsonResponse({'success': False, 'error':str(e)})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error':"Invalid request method"})


def list(request):
    trans = translate(language='ru')
    actual_url = request.path.split('/')[1]
    
    list_of_products = Products.objects.filter(Category__Types__Name_of_type = "Продукт", language = get_lang(trans=trans))
    
    context= {
        'list_of_products':list_of_products,
        'actual_url':actual_url,
    }

    return render(request, 'client_templates/pages/list.html', context)

def recips_list(request):
    actual_url = request.path.split('/')[2]
    user_id = request.user.id
    list_of_recips = Recips.objects.filter(staff = user_id)
    
    context= {
        'list_of_products':list_of_recips,
        'actual_url':actual_url,
    }

    return render(request, 'client_templates/pages/recips_list.html', context)

def recips_detail(request, id):
    user_id = request.user.id
    try:
        staff_object = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist as e:
        error = "Пользователь не найден!"
        return JsonResponse({'success': False, 'error':error})

    actual_url = []
    actual_url.append(request.path.split('/')[2])
    actual_url.append(request.path.split('/')[3])
    result = "/".join(actual_url)
    amoinacids = None
    product_id = Recips.objects.get(id=id)
    if staff_object.user_type == "3": 
        amoinacids = AminoAcidCompositionRecip.objects.get(recip=product_id)
    chemicals = ChemicalsRecip.objects.get(recip=product_id)
    context= {
        'product_id': product_id,
        'amoinacids': amoinacids,
        'chemicals': chemicals,
        "actual_url": result,
    }
        
    return render(request, 'client_templates/pages/recips_details.html',context)
