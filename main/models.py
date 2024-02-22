from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid, os, re

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Science Staff"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    
# Регионы
class RegionChoice(models.TextChoices):
    REGION_1 = "Чуйская область", "Чуйская область"
    REGION_2 = "Иссык-кульская область", "Иссык-кульская область"
    REGION_3 = "Ошская область", "Ошская область"
    REGION_4 = "Таласская область", "Таласская область"
    REGION_5 = "Нарынская область", "Нарынская область"
    REGION_6 = "Джалал-Абадская область", "Джалал-Абадская область"
    REGION_7 = "Баткенская область", "Баткенская область"
    ETALON = "Эталон", "Эталон"


class LanguageChoice(models.TextChoices):
    EN = "English", "English"
    RU = "Русский", "Русский"
    KG = "Кыргызча", "Кыргызча"

class Regions(models.Model):
    region = models.CharField(max_length=50, verbose_name='Регион')
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)

    def __str__(self):
        return  f"{self.region} - {self.language}"

# # Тип продуктов (Продукт, Ингредиент, Эталонный продукт и т.д.)
# class Types(models.Model):
#     Name_of_type = models.CharField(verbose_name='Наименование типа', max_length=75, help_text='(Продукт, Ингредиент, Эталонный продукт и т.д.)', null=True)
#     language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)
    
#     class Meta:
#         verbose_name = "Тип записи"
#     def __str__(self) -> str:
#         return f"{self.Name_of_type}"

# Категории продуктов (Мясные, Молочные, Хлебобулочные и т.д.)
class Categories(models.Model):
    Name_of_category = models.CharField(verbose_name='Наименование категории', max_length=75,help_text='(Мясные, Молочные, Хлебобулочные и т.д.)')
    Region = models.ForeignKey(Regions, on_delete=models.RESTRICT, related_name='regions_category')
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)
    class Meta:
        verbose_name = "Категория"
        
    def __str__(self):
        return f"{self.Name_of_category} - {self.Region}"
    
# Продукты
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    attribute_name = models.CharField(verbose_name='Наименование продукта', max_length=75)
    Category = models.ForeignKey(Categories, on_delete=models.RESTRICT, null=True, verbose_name='Категория продукта')
    date_analis = models.DateField(verbose_name='Дата исследования', default=timezone.now)
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)

    class Meta:
        verbose_name = ' -- Наименование продукта -- '
    
    def __str__(self):
        category_info = f"{self.Category.Region.region} - {self.Category.Name_of_category}" if self.Category else "N/A"
        return f"{self.attribute_name} - {category_info}"

# Виды Жирнокислоты
class FatAcids(models.Model):
    name = models.CharField(verbose_name='Название Жирнокислоты', max_length=40)  
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)

    class Meta:
        verbose_name = ' -- (Виды Жирнокислоты) -- '
    def __str__(self) -> str:
        return self.name
    
class FatAcidsTypeChoice(models.TextChoices):
    TYPE_1 = "Насыщенные жирные кислоты, %", "Насыщенные жирные кислоты, %"
    TYPE_2 = "Мононенасыщенные жирные кислоты, %", "Мононенасыщенные жирные кислоты, %"
    TYPE_3 = "Полиненасыщенные жирные кислоты, %", "Полиненасыщенные жирные кислоты, %"

class FatAcidsType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип жирнокислоты')
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)

    def __str__(self):
        return  f"{self.name} - {self.language}"
    
# Жирнокислотный Состав
class FatAcidCompositionOfMeal(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    types = models.ForeignKey(FatAcidsType, verbose_name='Тип жирных кислоты', on_delete=models.CASCADE)
    fat_acid = models.ForeignKey(FatAcids, on_delete=models.CASCADE, verbose_name='Вид жирнокислоты')
    value = models.FloatField(verbose_name='Содержание')
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)
    
    class Meta:
        verbose_name = ' -- (Жирнокислотный Состав) -- '

    
# Минеральный состав
class MineralComposition(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    Ca = models.FloatField(verbose_name='Ca (Кальций)', default=0)
    Na = models.FloatField(verbose_name='Na (Натрий)', default=0)
    K = models.FloatField(verbose_name='K (Калий)', default=0)
    P = models.FloatField(verbose_name='P (Фосфор)', default=0)
    Mn = models.FloatField(verbose_name='Mn (Марганец)', default=0)
    Zn = models.FloatField(verbose_name='Zn (Цинк)', default=0)
    Se = models.FloatField(verbose_name='Se (Скандий)', default=0)
    Cu = models.FloatField(verbose_name='Cu (Медь)', default=0)
    Fe = models.FloatField(verbose_name='Fe (Железо)', default=0)
    I = models.FloatField(verbose_name='I (Йод)', default=0)
    B = models.FloatField(verbose_name='B (Бор)', default=0)
    Li = models.FloatField(verbose_name='Li (Литий)', default=0)
    Al = models.FloatField(verbose_name='Al (Алюминий)', default=0)
    Mg = models.FloatField(verbose_name='Mg (Магний)', default=0)
    V = models.FloatField(verbose_name='V (Ванадий)', default=0)
    Ni = models.FloatField(verbose_name='Ni (Нитрий)', default=0)
    Co = models.FloatField(verbose_name='Co (Ковальт)', default=0)
    Cr = models.FloatField(verbose_name='Cr (Хром)', default=0)
    Sn = models.FloatField(verbose_name='Sn (Олово)', default=0)

    class Meta:
        verbose_name = ' -- (Минеральный состав) -- '
    
    def __str__(self) -> str:
        return self.product
    
# Аминокислотный состав
class AminoAcidComposition(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    asparing = models.FloatField(verbose_name='Аспарагиновая кислота', default=0)
    glutamin = models.FloatField(verbose_name='Глутаминовая кислота', default=0)
    serin = models.FloatField(verbose_name='Серин', default=0)
    gistidin = models.FloatField(verbose_name='Гистидин', default=0)
    glitsin = models.FloatField(verbose_name='Глицин', default=0)
    treonin = models.FloatField(verbose_name='Треонин', default=0)
    arginin = models.FloatField(verbose_name='Аргинин', default=0)
    alanin = models.FloatField(verbose_name='Аланин', default=0)
    tirosin = models.FloatField(verbose_name='Тирозин', default=0)
    tsistein = models.FloatField(verbose_name='Цистеин', default=0)
    valin = models.FloatField(verbose_name='Валин', default=0)
    metionin = models.FloatField(verbose_name='Метионин', default=0)
    triptofan = models.FloatField(verbose_name='Триптофан', default=0)
    fenilalalin = models.FloatField(verbose_name='Фенилаланин', default=0)
    izoleitsin = models.FloatField(verbose_name='Изолейцин', default=0)
    leitsin = models.FloatField(verbose_name='Лейцин', default=0)
    lisin = models.FloatField(verbose_name='Лизин', default=0)
    prolin = models.FloatField(verbose_name='Пролин', default=0)

    class Meta:
        verbose_name = ' -- (Аминокислотный Состав) -- '
    def __str__(self) -> str:
        return self.product
    
# Химический состав 
class Chemicals(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    soluable_solids = models.FloatField(verbose_name='Массовая доля растворимых сухих веществ, %', default=0)
    ascorbic_acids = models.FloatField(verbose_name='Массовая доля аскорбиновой кислоты, г/дм3', default=0)
    ash_content = models.FloatField(verbose_name='Зольность, %', default=0)
    moisture = models.FloatField(verbose_name='Массовая доля влаги, %', default=0)
    protein = models.FloatField(verbose_name='Массовая доля белка, %', default=0)
    fat = models.FloatField(verbose_name='Массовая доля жира, %', default=0)
    carbohydrates = models.FloatField(verbose_name='Массовая доля углевода, %', default=0)

    class Meta:
        verbose_name = ' -- (Химический состав) -- '

    def __str__(self) -> str:
        return self.product
        

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Recips(models.Model):
    name = models.CharField(max_length=85, verbose_name='Наименование рецептуры')
    cost_price_100gramm = models.FloatField(verbose_name='Себестоимость', default=0)
    cost_price_1kg = models.FloatField(verbose_name='Себестоимость', default=0)
    date_analis = models.DateTimeField(verbose_name='Дата проектирования', default=timezone.now)
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, verbose_name='Язык', choices=LanguageChoice.choices, default=LanguageChoice.RU)

# Аминокислотный состав
class AminoAcidCompositionRecip(models.Model):
    recip = models.ForeignKey(Recips, on_delete=models.CASCADE, null=True)
    izoleitsin = models.FloatField(verbose_name='Изолейцин', default=0)
    leitsin = models.FloatField(verbose_name='Лейцин', default=0)
    lisin = models.FloatField(verbose_name='Лизин', default=0)
    valin = models.FloatField(verbose_name='Валин', default=0)
    metilcistein = models.FloatField(verbose_name='Метилцистеин', default=0)
    feniltirosin = models.FloatField(verbose_name='Фенилтиросин', default=0)
    triptofan = models.FloatField(verbose_name='Триптофан', default=0)
    treon = models.FloatField(verbose_name='Треон', default=0)
    izoleitsin1 = models.FloatField(verbose_name='Изолейцин C, %', default=0)
    leitsin1 = models.FloatField(verbose_name='Лейцин C, %', default=0)
    lisin1 = models.FloatField(verbose_name='Лизин C, %', default=0)
    valin1 = models.FloatField(verbose_name='Валин C, %', default=0)
    metilcistein1 = models.FloatField(verbose_name='Метилцистеин C, %', default=0)
    feniltirosin1 = models.FloatField(verbose_name='Фенилтиросин C, %', default=0)
    triptofan1 = models.FloatField(verbose_name='Триптофан C, %', default=0)
    treon1 = models.FloatField(verbose_name='Треон C, %', default=0)
    izoleitsin_a = models.FloatField(verbose_name='Изолейцин a, %', default=0)
    leitsin_a = models.FloatField(verbose_name='Лейцин a, %', default=0)
    lisin_a = models.FloatField(verbose_name='Лизин a, %', default=0)
    valin_a = models.FloatField(verbose_name='Валин a, %', default=0)
    metilcistein_a = models.FloatField(verbose_name='Метилцистеин a, %', default=0)
    feniltirosin_a = models.FloatField(verbose_name='Фенилтиросин a, %', default=0)
    triptofan_a = models.FloatField(verbose_name='Триптофан a, %', default=0)
    treon_a = models.FloatField(verbose_name='Треон a, %', default=0)
    c_min = models.FloatField(verbose_name='Cmin', default=0)

    class Meta:
        verbose_name = ' -- (Аминокислотный Состав) -- '
    def __str__(self) -> str:
        return self.recip
    
# Химический состав 
class ChemicalsRecip(models.Model):
    recip = models.ForeignKey(Recips, on_delete=models.CASCADE, null=True)
    protein = models.FloatField(verbose_name='Массовая доля белка, %', default=0)
    fat = models.FloatField(verbose_name='Массовая доля жира, %', default=0)
    carbohydrates = models.FloatField(verbose_name='Массовая доля углевода, %', default=0)
    kkal = models.FloatField(verbose_name='ккал', default=0)
    kJ = models.FloatField(verbose_name='кДж', default=0)

    class Meta:
        verbose_name = ' -- (Химический состав) -- '

    def __str__(self) -> str:
        return self.recip
    

class Ingredients(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    mass_fraction = models.FloatField(verbose_name='Массовая доля в рецепте', default=0)
    recip = models.ForeignKey(Recips, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product
