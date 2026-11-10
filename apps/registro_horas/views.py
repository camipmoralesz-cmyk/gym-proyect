from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva

@login_required

def lista_horarios(request):
    # Vista principal del calendario semanal de afluencia/horarios
    return render(request, 'registro_horas/horarios_lista.html')

def detalle_horario(request, pk):
    # Vista de detalle para un bloque horario específico (Segunda pantalla)
    return render(request, 'registro_horas/horarios_detalle.html')

def crear_horario(request):
    # Vista para crear un nuevo bloque horario/cupos
    return render(request, 'registro_horas/horarios_form.html')

def editar_horario(request, pk):
    # Vista visual para editar un bloque horario existente
    return render(request, 'registro_horas/horarios_editar.html')

def horarios_view(request):
    # Aquí puedes pasar datos en el context si los necesitas luego
    return render(request, 'registro_horas/horarios.html')

def realizar_reserva(request, bloque_id):
    # Aquí recibimos el bloque que el cliente quiere reservar
    # Guardamos en la base de datos que este usuario reservó este bloque
    Reserva.objects.get_or_create(
        usuario=request.user,
        bloque_horario=bloque_id
    )
    return redirect('registro_horas:horarios')
    
    
