from rest_framework import serializers

from accounts.serializers import TraderSerializer
from panels import models


class DiscountSerializer(serializers.ModelSerializer):
    trader_username = serializers.CharField(source='trader.user.username')

    class Meta:
        model = models.Discount
        fields = '__all__'
