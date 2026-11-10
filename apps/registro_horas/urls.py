from django.urls import path
from . import views

app_name = 'registro_horas'

urlpatterns = [
    path('lista', views.lista_horarios, name='lista_horarios'),
    path('', views.horarios_view, name='horarios'),
    path('detalle/<int:pk>/', views.detalle_horario, name='detalle_horario'),
<<<<<<< HEAD
    path('crear/', views.crear_horario, name='crear_horario'),
    path('editar/<int:pk>/', views.editar_horario, name='editar_horario'),
    path('eliminar/<int:pk>/', views.eliminar_horario, name='eliminar_horario'),
]
=======
    path('nuevo/', views.crear_horario, name='crear_horario'),
    path('crear/<str:bloque_id>/', views.realizar_reserva, name='realizar_reserva'),
    path('detalle/editar/<int:pk>/', views.editar_horario, name='editar_horario'),
]

>>>>>>> ramaJessica
