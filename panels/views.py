from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from accounts.models import POSTerminal, Trader, Client
from accounts.serializers import TraderSerializer, TerminalSerializer
from panels.filters import DiscountsFilter
from panels.models import Discount
from panels.serializers import DiscountSerializer, EmployeeDiscountSerializer, EmployeeDiscountActionSerializer

from panels import mixins


# ADMIN PANEL 1


class TradersPanelView(mixins.TraderPermissionMixin, ListCreateAPIView):
    serializer_class = DiscountSerializer
    filterset_class = DiscountsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        trader = Trader.objects.get(user=self.request.user)
        return Discount.objects.filter(trader=trader)

    def perform_create(self, serializer):
        serializer.save(trader=self.request.user.trader)


class TradersPanelChangeNotifStatus(mixins.TraderPermissionMixin, APIView):
    def post(self, request, *args, **kwargs):
        trader = self.request.user.trader
        trader.notifications_status = not trader.notifications_status
        trader.save()

        return HttpResponse('Notification status changed')

    def get(self, request, *args, **kwargs):
        trader = self.request.user.trader
        return HttpResponse({'state': trader.notifications_status})


# ADMIN PANEL 2


class EmployeesPanelGetTraders(mixins.EmployeePermissionMixin, ListAPIView):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer


class EmployeesPanelGetOffers(mixins.EmployeePermissionMixin, ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class EmployeesPanelGetWaitingOffers(mixins.EmployeePermissionMixin, ListCreateAPIView):
    queryset = Discount.objects.filter(status='Waiting')
    serializer_class = EmployeeDiscountSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeDiscountActionSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.bankemployee)


class EmployeesPanelGetTerminals(mixins.EmployeePermissionMixin, ListAPIView):
    queryset = POSTerminal.objects.all()
    serializer_class = TerminalSerializer


# ADMIN PANEL 3


class ClientsPanelView(mixins.CardholderPermissionMixin, ListAPIView):
    queryset = Discount.objects.filter(status='Active')
    serializer_class = DiscountSerializer


class ClientsPanelChangeNotifStatus(mixins.CardholderPermissionMixin, APIView):
    def post(self, request, *args, **kwargs):
        client = self.request.user.client
        client.notifications_status = not client.notifications_status
        client.save()

        return HttpResponse({'status': 'Notification status changed'})

    def get(self, request, *args, **kwargs):
        client = self.request.user.client
        return HttpResponse({'state': client.notifications_status})
