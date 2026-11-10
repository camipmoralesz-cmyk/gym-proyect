from django.db import models
from django.contrib.auth.models import User

class Maquina(models.Model):
    idMaquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    instruccionesUso = models.TextField(blank=True, null=True)
    estadoDisponible = models.BooleanField(default=True)  # True = Disponible, False = En Mantención
    idAdministrador = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idAdministrador')

    class Meta:
        db_table = 'Maquina'  # Vincula exactamente con la tabla de la base de datos

    def __str__(self):
        return self.nombre