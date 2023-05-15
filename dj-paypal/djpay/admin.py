from django.contrib import admin
from .models import Scopes,PaypalToken


# Register your models here.
@admin.register(Scopes)
class ScopesAdmin(admin.ModelAdmin):
    pass

@admin.register(PaypalToken)
class PaypalTokenAdmin(admin.ModelAdmin):
    pass
