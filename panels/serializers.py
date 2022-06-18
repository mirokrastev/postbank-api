from rest_framework import serializers

from accounts.serializers import TraderSerializer
from panels import models


class DiscountSerializer(serializers.ModelSerializer):
    trader = TraderSerializer()

    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent', 'start_date', 'end_date', 'status', 'is_processed', 'trader')
