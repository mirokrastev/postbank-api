from django.urls import path
from panels import views

urlpatterns = [
    # Panel 1
    path('api/traders/', views.TradersPanelView.as_view(), name='traders'),

    # Panel 2
    path('api/employees/traders/', views.EmployeesPanelGetTraders.as_view(), name='employees_traders'),
    path('api/employees/terminals/', views.EmployeesPanelGetTerminals.as_view(), name='employees_terminals'),
    path('api/employees/offers/', views.EmployeesPanelGetOffers.as_view(), name='employees_offers'),
    path('api/employees/waiting_offers/', views.EmployeesPanelGetWaitingOffers.as_view(),
         name='employees_waiting_offers'),

    # Panel 3
    path('api/clients/', views.ClientsPanelView.as_view(), name='clients_offers'),
    path('api/clients/notif/', views.ClientsPanelChangeNotifStatus.as_view(), name='clients_notif_status'),
]
