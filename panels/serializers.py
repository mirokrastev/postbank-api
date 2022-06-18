from rest_framework import serializers

from accounts.serializers import TraderSerializer
from panels import models


class DiscountSerializer(serializers.ModelSerializer):
    trader = TraderSerializer()

    class Meta:
        model = models.Discount
        fields = '__all__'
