from django.contrib import admin
from .models import Scope, PaypalToken, PaypalInfo
from django.conf import settings
from django.apps import apps


# Register your models here.
@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass


@admin.register(PaypalToken)
class PaypalTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(PaypalInfo)
class PaypalInfoRegisterAdmin(admin.ModelAdmin):
    pass
