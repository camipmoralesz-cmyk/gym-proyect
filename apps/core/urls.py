from django.urls import path
from .views import admin_login_view, dashboard_core_view, registro_view, test_cliente_view

app_name = 'core'

urlpatterns = [
    path('', admin_login_view, name='login'),               
    path('dashboard/', dashboard_core_view, name='dashboard'),
    path('registro/', registro_view, name='registro'), 
    #Para saber si sirve la base cliente
    path('vista-cliente/', test_cliente_view, name='test_cliente'), # <- Ruta de prueba temporal
]