from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('gestion/', views.lista_maquinas_admin, name='gestion_maquinas'),
    path('gestion/nuevo/', views.crear_maquina, name='crear_maquina'),
    path('gestion/editar/<int:pk>/', views.editar_maquina, name='editar_maquina'),
    
    # Ruta para el catálogo del cliente
    path('', views.catalogo_maquinas_view, name='catalogo_maquinas'),
    path('gestion/eliminar/<int:pk>/', views.eliminar_maquina, name='eliminar_maquina'),
]