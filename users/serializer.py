from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payments = UserSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
