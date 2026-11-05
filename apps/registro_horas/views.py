from django.shortcuts import render

def lista_horarios(request):
    # Vista principal del calendario semanal de afluencia/horarios
    return render(request, 'registro_horas/horarios_lista.html')

def detalle_horario(request, pk):
    # Vista de detalle para un bloque horario específico (Segunda pantalla)
    return render(request, 'registro_horas/horarios_detalle.html')

def crear_horario(request):
    # Vista para crear un nuevo bloque horario/cupos
    return render(request, 'registro_horas/horarios_form.html')