from django.urls import path
from . import views
from .views import (
    login_view, 
    dashboard_core_view, 
    registro_view, 
    test_cliente_view
)

app_name = 'core'

urlpatterns = [
    path('', login_view, name='login'),                     
    path('dashboard/', dashboard_core_view, name='dashboard'),
    path('registro/', registro_view, name='registro'), 
    path('vista-cliente/', test_cliente_view, name='test_cliente'), # <- Ruta de prueba temporal
    path('logout/', views.logout_view, name='logout'),
]