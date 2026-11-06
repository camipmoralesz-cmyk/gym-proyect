from django.db import models

class Horario(models.Model):
    idHorario = models.AutoField(primary_key=True)
    diaSemana = models.CharField(max_length=20)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    capacidadMaxima = models.IntegerField()
    cuposOcupados = models.IntegerField(default=0)
    fecha = models.DateField(null=True, blank=True)

    @property
    def cupos_disponibles(self):
        return self.capacidadMaxima - self.cuposOcupados

    class Meta:
        managed = False
        db_table = 'Horario'