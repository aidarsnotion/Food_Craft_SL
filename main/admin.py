from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
