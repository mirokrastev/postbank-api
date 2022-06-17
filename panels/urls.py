from django.urls import path
from panels import views

urlpatterns = [
    path('api/traders/', views.TradersPanelView.as_view(), name='traders'),
    path('api/clients/', views.ClientsPanelView.as_view(), name='clients_offers'),
    path('api/employees/traders/', views.EmployeesPanelGetTraders.as_view(), name='employees_traders'),
    path('api/employees/terminals/', views.EmployeesPanelGetTerminals.as_view(), name='employees_terminals'),
    path('api/employees/offers/', views.EmployeesPanelGetOffers.as_view(), name='employees_offers'),
]