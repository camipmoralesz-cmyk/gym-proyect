from django.urls import path
from . import views

app_name = 'registro_horas'

urlpatterns = [
    path('', views.lista_horarios, name='lista_horarios'),
    path('detalle/<int:pk>/', views.detalle_horario, name='detalle_horario'),
    path('nuevo/', views.crear_horario, name='crear_horario'),
]