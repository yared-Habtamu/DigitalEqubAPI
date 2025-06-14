from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at', 'chapa_response')


class PaymentCallbackSerializer(serializers.Serializer):
    tx_ref = serializers.CharField()
    status = serializers.CharField()
