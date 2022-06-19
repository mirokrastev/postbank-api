from django_filters import rest_framework as filters

from panels.models import Discount


class DiscountsFilter(filters.FilterSet):
    start_date = filters.DateFilter(lookup_expr='gte')
    end_date = filters.DateFilter(lookup_expr='lte')

    class Meta:
        model = Discount
        fields = ('status', 'start_date', 'end_date')
