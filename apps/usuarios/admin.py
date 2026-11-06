from django.contrib import admin
from .models import Usuario, Cliente, Administrador


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['idUsuario', 'nombre', 'correo']
    search_fields = ['nombre', 'correo']


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['idUsuario', 'fechaVencimientoMembrecia']
    search_fields = ['idUsuario__nombre', 'idUsuario__correo']


class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['idUsuario', 'nivelPermiso']
    list_filter = ['nivelPermiso']
    search_fields = ['idUsuario__nombre']


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Administrador, AdministradorAdmin)