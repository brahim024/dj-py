from django.contrib import admin
from .models import Scope, PaypalToken, PaypalInfo


# Register your models here.
@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass


@admin.register(PaypalToken)
class PaypalTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(PaypalInfo)
class PaypalInfoRegister(admin.ModelAdmin):
    pass
