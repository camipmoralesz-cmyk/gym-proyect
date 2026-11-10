from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos complementarios del User de Django (RUT y teléfono)."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='perfil')
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut})"


class Cliente(models.Model):
    # Estado con opciones cerradas (choices), pedido por la pauta
    ESTADOS = [('activo', 'Activo'), ('desactivado', 'Desactivado')]

    idUsuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        primary_key=True, db_column='idUsuario', related_name='cliente')
    fechaVencimientoMembrecia = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return f"Cliente: {self.idUsuario.get_full_name()}"


class Administrador(models.Model):
    idUsuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        primary_key=True, db_column='idUsuario', related_name='administrador')
    nivelPermiso = models.CharField(max_length=50)

    class Meta:
        db_table = 'Administrador'

    def __str__(self):
        return f"Admin: {self.idUsuario.get_full_name()} - {self.nivelPermiso}"