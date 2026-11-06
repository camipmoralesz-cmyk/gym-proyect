from django.db import models
from django.conf import settings

class Maquina(models.Model):
    idMaquina = models.AutoField(primary_key=True)                  # Código único que identifica a cada máquina en el sistema
    nombre = models.CharField(max_length=100)                       # Nombre o título de la máquina del gimnasio
    descripcion = models.TextField(blank=True, null=True)           # Breve detalle o características de la máquina (opcional)
    instruccionesUso = models.TextField(blank=True, null=True)      # Indicaciones sobre cómo se debe usar correctamente (opcional)
    estadoDisponible = models.BooleanField(default=True)            # Indica si la máquina se encuentra habilitada para uso (por defecto está disponible)
    imagen = models.CharField(max_length=255, blank=True, null=True)# Archivo o ruta de la fotografía asociada a la máquina (opcional)
    
    # Apunta directamente al modelo de usuario de Django
    idAdministrador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='idAdministrador'
    )

    class Meta:
        db_table = 'Maquina' # Esto le dice a Django que use la tabla 'Maquina' que ya creaste en MySQL