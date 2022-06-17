from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts import models


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Trader)
admin.site.register(models.BankEmployee)
admin.site.register(models.POSTerminal)
admin.site.register(models.Client)
