from .models import *
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea, DateInput
from django import forms
from django.contrib.auth.models import User, AnonymousUser, Permission
import re
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес электронной почты',
        'type': 'email',
        'name': 'email',
        'id': 'id_email',
        }))

class UserSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите новый пароль',
        'type': 'password',
        'name': 'password1',
        'id': 'id_pass1',
        'strip': 'False',
        })
    )

    new_password2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль еще раз',
        'type': 'password',
        'name': 'password2',
        'id': 'id_pass2',
        })
    )

# Форма для профиля   
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email', 'user_type']
        
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "last_name", "placeholder" : "Введите Имя"}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "first_name", "placeholder" : "Введите Фамилию"}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "username", "placeholder" : "Введите Имя Пользователя"}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', "id" : "email", "placeholder" : "Введите E-mail"}))
    user_type = forms.ChoiceField(choices=[             
            ((1, "HOD"), (2, "Staff"), (3, "Science Staff")),       
            ], widget= forms.Select(attrs={"class" : "form-control", "id" : "language"}), required=True) 


class RegionsForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ['region', 'language']
    
    region = forms.CharField(max_length=50, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "region", "placeholder" : "Введите название региона", "size" : 50},
            ))
    language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            ) 


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['attribute_name', 'Category', 'date_analis', 'language']
    
    attribute_name = forms.CharField(max_length=80, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Введите наименование ингредиента", "size" : 80},
            ))
    Category = forms.ModelChoiceField(queryset=Categories.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "Category"},
            ))
    date_analis = forms.DateField(required=False, 
                               widget=DateInput(
                                   attrs={"type" : "date", "class" : "form-control", 'required': True, "id" : "date_analis"}
                                   )
                               )
    language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            )     
    

# class TypesForm(forms.ModelForm):
#     class Meta:
#         model = Types
#         fields = ['Name_of_type', 'language']
    
#     Name_of_type = forms.CharField(max_length=80, required=True, widget=TextInput(
#             attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Введите наименование типа", "size" : 80},
#             ))
#     language = forms.ChoiceField(
#                                 choices=LanguageChoice.choices,
#                                 widget= forms.Select(
#                                         attrs={"class" : "form-control", "id" : "language"}
#                                     ),
#                                 required=True
#                             )     
    
    
    
class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['Name_of_category', 'Region', 'language']
    
    Name_of_category = forms.CharField(max_length=80, required=True, widget=TextInput(
            attrs={"class" : "form-control", "id" : "title", "placeholder" : "Введите категорию", "size" : 80},
            ))
    Region = forms.ModelChoiceField(queryset=Regions.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "Region"},
            ))
    language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            )     

class FatAcidsForm(forms.ModelForm):
    class Meta:
        model = FatAcids
        fields = ['name']
    
    name = forms.CharField(max_length=40, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "C8:0", "size" : 80},
            ))

class FatAcidsTypeForm(forms.ModelForm):
    class Meta:
        model = FatAcidsType
        fields = ['name', 'language']
    
    name = forms.CharField(max_length=50, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Насыщенные, Мононенасыщенные и т.д.", "size" : 80},
            ))
    language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            ) 

class FatAcidCompositionForm(forms.ModelForm):
    class Meta:
        model = FatAcidCompositionOfMeal
        fields = ['product', 'types', 'fat_acid', 'value', 'language']
    
    product = forms.ModelChoiceField(queryset=Products.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "product"},
            ))
    types = forms.ModelChoiceField(queryset=FatAcidsType.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "types"},
            ))
    value = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))

    fat_acid = forms.ModelChoiceField(queryset=FatAcids.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "fat_acid"},
            ))
    
    language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            )    
      
class MineralForm(forms.ModelForm):
    class Meta:
        model = MineralComposition
        fields = ['product', 'Ca', 'Na', 'K', 'P', 'Mn',
                    'Zn', 'Se', 'Cu', 'Fe', 'I', 'B', 'Li',
                    'Al', 'Mg', 'V', 'Ni', 'Co', 'Cr', 'Sn']
    
    product = forms.ModelChoiceField(queryset=Products.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "product"},
            ))
    
    Ca = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Na = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    K = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    P = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Mn = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Zn = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Se = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Cu = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Fe = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    I = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    B = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Li = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Al = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Mg = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    V = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Ni = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Co = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Cr = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    Sn = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001, 'max': 10000, 'min': 0.00001}))
    

class AminoAcidsForm(forms.ModelForm):
    class Meta:
        model = AminoAcidComposition
        fields = ['product', 'asparing', 'glutamin', 'serin', 'gistidin', 'glitsin', 'treonin', 'arginin', 'alanin',
                  'tirosin', 'tsistein', 'valin', 'metionin', 'triptofan', 'fenilalalin', 'izoleitsin', 'leitsin', 'lisin', 'prolin']
    
    product = forms.ModelChoiceField(queryset=Products.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "product"},
            ))
    
    asparing = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    glutamin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    serin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    gistidin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    glitsin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    treonin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    arginin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    alanin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    tirosin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    tsistein = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    valin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    metionin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    triptofan = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    fenilalalin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    izoleitsin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    leitsin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    lisin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    prolin = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    
class ChemicalsForm(forms.ModelForm):
    class Meta:
        model = Chemicals
        fields = ['product', 'soluable_solids', 'ascorbic_acids', 'ash_content', 'moisture', 'protein', 'fat', 'carbohydrates']
    
    product = forms.ModelChoiceField(queryset=Products.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "product"},
            ))
    
    soluable_solids = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    ascorbic_acids = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    ash_content = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    moisture = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    protein = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    fat = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))
    carbohydrates = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.00001,'min': 0.0}))


class RecipsForm(forms.ModelForm):
    class Meta:
        model = Recips
        fields = ['name', 'cost_price_100gramm', 'cost_price_1kg']
    
    name = forms.CharField(max_length=80, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Введите наименование рецепта", "size" : 85},
            ))
    
    cost_price_100gramm = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.01,'min': 0.001}))
    cost_price_1kg = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.01,'min': 0.001}))
    

class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['product', 'mass_fraction', 'recip']
    
    product = forms.ModelChoiceField(queryset=Products.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "product"},
            ))
    
    mass_fraction = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.01,'min': 0.001}))
    
    recip = forms.ModelChoiceField(queryset=Recips.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "recip"},
            ))