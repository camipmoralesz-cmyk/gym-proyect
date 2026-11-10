from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva, Horario
from datetime import datetime, timedelta

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
# Obtenemos la fecha de referencia de la URL (ej: ?fecha=2026-04-06)
    fecha_param = request.GET.get('fecha')
    
    if fecha_param:
        try:
            ref_date = datetime.strptime(fecha_param, '%Y-%m-%d').date()
        except ValueError:
            ref_date = datetime.now().date()
    else:
        ref_date = datetime.now().date()

    # Calculamos el Lunes y el Domingo de esa semana específica
    start_of_week = ref_date - timedelta(days=ref_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Fechas para los botones de navegación de semanas
    prev_week_date = (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d')
    next_week_date = (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d')

    # Filtrar estrictamente los horarios de la base de datos para este rango de semana
    horarios_semana = Horario.objects.filter(fecha__range=[start_of_week, end_of_week])

    context = {
        # Listas filtradas por día de la semana
        'lunes': horarios_semana.filter(diaSemana__iexact='Lunes'),
        'martes': horarios_semana.filter(diaSemana__iexact='Martes'),
        'miercoles': horarios_semana.filter(diaSemana__iexact='Miércoles'),
        'jueves': horarios_semana.filter(diaSemana__iexact='Jueves'),
        'viernes': horarios_semana.filter(diaSemana__iexact='Viernes'),
        'sabado': horarios_semana.filter(diaSemana__iexact='Sábado'),
        'domingo': horarios_semana.filter(diaSemana__iexact='Domingo'),
        
        # Fechas individuales para los títulos de cada columna de la grilla
        'start_of_week': start_of_week,
        'lunes_fecha': start_of_week,
        'martes_fecha': start_of_week + timedelta(days=1),
        'miercoles_fecha': start_of_week + timedelta(days=2),
        'jueves_fecha': start_of_week + timedelta(days=3),
        'viernes_fecha': start_of_week + timedelta(days=4),
        'sabado_fecha': start_of_week + timedelta(days=5),
        'domingo_fecha': start_of_week + timedelta(days=6),
        
        # Parámetros para los botones de navegación
        'prev_week_date': prev_week_date,
        'next_week_date': next_week_date,
    }
    
    # Reemplaza 'portal_clientes/horarios.html' por la ruta del template que usa tu compañera
    return render(request, 'registro_horas/horarios.html', context)

def realizar_reserva(request, bloque_id):
    # Aquí recibimos el bloque que el cliente quiere reservar
    # Guardamos en la base de datos que este usuario reservó este bloque
    Reserva.objects.get_or_create(
        usuario=request.user,
        bloque_horario=bloque_id
    )
    return redirect('registro_horas:horarios')
    
    
