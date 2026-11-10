from django.urls import path
from .views import (
    login_view, 
    dashboard_core_view, 
    registro_view, 
    test_cliente_view)

app_name = 'core'

#urlpatterns = [
    #path('', login_view, name='login'),  
    #path('admin-login/', admin_login_view, name='admin_login'),             
    #path('dashboard/', dashboard_core_view, name='dashboard'),
    #path('registro/', registro_view, name='registro'), 
    #Para saber si sirve la base cliente
    #path('login-cliente/', login_cliente_view, name='login_cliente'),
    #path('vista-cliente/', test_cliente_view, name='test_cliente'), # <- Ruta de prueba temporal
#]


app_name = 'core'

urlpatterns = [
    path('', login_view, name='login'),                 
    path('dashboard/', dashboard_core_view, name='dashboard'),
    path('registro/', registro_view, name='registro'), 
    path('vista-cliente/', test_cliente_view, name='test_cliente'), # <- Ruta de prueba temporal
]