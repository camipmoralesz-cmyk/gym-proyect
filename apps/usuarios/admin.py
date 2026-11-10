from django.contrib import admin
from .models import Perfil, Cliente, Administrador


# ============================================================
# Perfil: datos complementarios del User (RUT y teléfono)
# ============================================================
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'telefono')       # columnas de la tabla
    search_fields = ('rut', 'user__email', 'user__first_name', 'user__last_name')


# ============================================================
# Cliente: membresía y estado (baja lógica)
# ============================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idUsuario', 'fechaVencimientoMembrecia', 'estado')
    list_filter = ('estado',)                         # filtro lateral
    search_fields = ('idUsuario__email', 'idUsuario__first_name', 'idUsuario__last_name')
    list_editable = ('estado',)                       # edición rápida en la grilla
    fieldsets = (
        ('Cuenta', {'fields': ('idUsuario',)}),
        ('Membresía', {'fields': ('fechaVencimientoMembrecia', 'estado')}),
    )


# ============================================================
# Administrador: nivel de permiso
# ============================================================
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('idUsuario', 'nivelPermiso')
    list_filter = ('nivelPermiso',)
    search_fields = ('idUsuario__email', 'idUsuario__first_name')