from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView

from accounts.models import POSTerminal, Trader
from accounts.serializers import TerminalSerializer, TraderSerializer
from panels.models import Discount
from panels.serializers import DiscountSerializer

# ADMIN PANEL 1


class TradersPanelView(ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


# ADMIN PANEL 2


class EmployeesPanelGetTraders(ListAPIView):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer


class EmployeesPanelGetTerminals(ListAPIView):
    queryset = POSTerminal.objects.all()
    serializer_class = TerminalSerializer


class EmployeesPanelGetOffers(ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


# ADMIN PANEL 3

class ClientsPanelView(ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class ClientsPanelView2(ListAPIView):
    ...
