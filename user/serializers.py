from rest_framework import serializers
from .models import Payment  # или откуда у тебя эта модель

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'