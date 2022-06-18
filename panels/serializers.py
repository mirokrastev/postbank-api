from rest_framework import serializers

from accounts.serializers import TraderSerializer
from panels import models


class DiscountSerializer(serializers.ModelSerializer):
    trader = TraderSerializer()

    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent', 'start_date', 'end_date', 'status', 'is_processed', 'trader')


class EmployeeDiscountActionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='discount.status', read_only=True)

    class Meta:
        model = models.EmployeeDiscountAction
        fields = ('discount', 'state', 'status')
