from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=255)

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

    def save(self, *args, **kwargs):
        # Verifica si ya es un hash válido de Django; si no lo es, lo encripta
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
            
        super().save(*args, **kwargs)


class Cliente(models.Model):
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='idUsuario'
    )
    fechaVencimientoMembrecia = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"Cliente: {self.idUsuario.nombre}"


class Administrador(models.Model):
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='idUsuario'
    )
    nivelPermiso = models.CharField(max_length=50)

    class Meta:
        db_table = 'Administrador'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return f"Admin: {self.idUsuario.nombre} - {self.nivelPermiso}"