from rest_framework import serializers

from accounts.serializers import TraderSerializer
from panels import models


class DiscountSerializer(serializers.ModelSerializer):
    trader = TraderSerializer(read_only=True)
    status = serializers.ChoiceField(choices=models.Discount.STATUS_OPTS, required=False, read_only=True)

    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent', 'start_date', 'end_date', 'status', 'trader')


class EmployeeDiscountSerializer(DiscountSerializer):
    has_voted = serializers.SerializerMethodField()

    def get_has_voted(self, instance):
        request = self.context.get('request')
        if request is None:
            return False

        employee = request.user.bankemployee
        return models.EmployeeDiscountAction.objects.filter(discount=instance, employee=employee).count() > 0

    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent', 'start_date', 'end_date', 'status', 'has_voted', 'trader')


class EmployeeDiscountActionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='discount.status', read_only=True)

    class Meta:
        model = models.EmployeeDiscountAction
        fields = ('discount', 'state', 'status')
