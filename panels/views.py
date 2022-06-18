from http.client import HTTPResponse

from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import POSTerminal, Trader, Client
from accounts.serializers import TerminalSerializer, TraderSerializer, ClientSerializer
from panels.models import Discount
from panels.serializers import DiscountSerializer

# ADMIN PANEL 1


class TradersPanelView(ListCreateAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.filter(trader=self.request.user.trader)


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


class ClientsPanelChangeNotifStatus(APIView):
    def post(self, request):
        user_obj = Client.objects.get(user=request.user)
        if user_obj.notifications_status:
            user_obj.notifications_status = False
        else:
            user_obj.notifications_status = True
        user_obj.save()

        return HttpResponse('Notification status changed')

    def get(self, request):
        user_obj = Client.objects.get(user=request.user)
        return HttpResponse(f'{user_obj.notifications_status}')
