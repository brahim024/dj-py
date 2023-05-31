from rest_framework import serializers
from .models import Scope,PaypalToken,PaypalInfo

class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = '__all__'

