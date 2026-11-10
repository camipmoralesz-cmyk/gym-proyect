from django.db import models
from django.contrib.auth.models import User

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bloque_horario = models.CharField(max_length=50) # Ejemplo: "Lunes 6 - 09:00 hrs"
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.bloque_horario}"