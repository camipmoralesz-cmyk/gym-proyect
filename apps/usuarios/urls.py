from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    logout_view,
    gestion_usuarios_view,
    crear_usuario_view,
    editar_usuario_view,
    eliminar_usuario_view,
    cambiar_estado_cliente_view,
)

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('gestion/', gestion_usuarios_view, name='gestion_usuarios'),
    path('crear/', crear_usuario_view, name='crear_usuario'),
    path('editar/<int:id>/', editar_usuario_view, name='editar_usuario'),
    path('eliminar/<int:id>/', eliminar_usuario_view, name='eliminar_usuario'),
    path('gestion/estado/<int:id>/', cambiar_estado_cliente_view, name='cambiar_estado'),
]