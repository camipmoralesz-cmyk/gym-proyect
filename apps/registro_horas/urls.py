from django.urls import path
from . import views

app_name = 'registro_horas'

urlpatterns = [
    path('', views.lista_horarios, name='lista_horarios'),
    path('detalle/<int:pk>/', views.detalle_horario, name='detalle_horario'),
    path('crear/', views.crear_horario, name='crear_horario'),
    path('editar/<int:pk>/', views.editar_horario, name='editar_horario'),
    path('eliminar/<int:pk>/', views.eliminar_horario, name='eliminar_horario'),
]