from django.db import models
from django.contrib.auth.models import User

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bloque_horario = models.CharField(max_length=50) # Ejemplo: "Lunes 6 - 09:00 hrs"
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.bloque_horario}"

class Horario(models.Model):
    idHorario = models.AutoField(primary_key=True)
    diaSemana = models.CharField(max_length=20)
    fecha = models.DateField(null=True, blank=True)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    capacidadMaxima = models.IntegerField(default=15)
    cuposOcupados = models.IntegerField(default=0)

    @property
    def cupos_disponibles(self):
        return max(0, self.capacidadMaxima - self.cuposOcupados)

    def __str__(self):
        return f"{self.diaSemana} ({self.horaInicio} - {self.horaFin})"

    class Meta:
        db_table = 'horario'  # <--- Esto le indica a Django que use exactamente la tabla 'horario' de tu BD