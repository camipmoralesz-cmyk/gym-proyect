from django.db import models
from django.conf import settings

class Maquina(models.Model):
    idMaquina = models.AutoField(primary_key=True)                    # Código único que identifica a cada máquina en el sistema
    nombre = models.CharField(max_length=100)                         # Nombre o título de la máquina del gimnasio
    descripcion = models.TextField(blank=True, null=True)             # Breve detalle o características de la máquina (opcional)
    instruccionesUso = models.TextField(blank=True, null=True)        # Indicaciones sobre cómo se debe usar correctamente (opcional)
    estadoDisponible = models.BooleanField(default=True)              # Indica si la máquina se encuentra habilitada para uso
    imagen = models.CharField(max_length=255, blank=True, null=True)  # Archivo o ruta de la fotografía asociada a la máquina
    
    # Apunta directamente al modelo de usuario de Django configurado en el proyecto
    idAdministrador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='idAdministrador'
    )

    class Meta:
        db_table = 'Maquina' # Vincula exactamente con la tabla 'Maquina' de tu base de datos MySQL

    def __str__(self):
        return self.nombre