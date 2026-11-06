from django.db import models
from django.conf import settings

class Maquina(models.Model):
    idMaquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    instruccionesUso = models.TextField(blank=True, null=True)
    estadoDisponible = models.BooleanField(default=True)
    
    # Apunta directamente al modelo de usuario de Django
    idAdministrador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='idAdministrador'
    )

    class Meta:
        db_table = 'Maquina' # Esto le dice a Django que use la tabla 'Maquina' que ya creaste en MySQL