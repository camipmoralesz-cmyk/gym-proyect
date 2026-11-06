from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Horario
from django.contrib.auth import authenticate

@login_required(login_url='login')
def lista_horarios(request):
    # Obtenemos la fecha de referencia desde los parámetros GET (ej: ?fecha=2026-04-06)
    fecha_param = request.GET.get('fecha')
    
    if fecha_param:
        try:
            ref_date = datetime.strptime(fecha_param, '%Y-%m-%d').date()
        except ValueError:
            ref_date = datetime.now().date()
    else:
        ref_date = datetime.now().date()

    # Calculamos el Lunes y el Domingo de esa semana específica
    # weekday(): Lunes es 0, Domingo es 6
    start_of_week = ref_date - timedelta(days=ref_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Calculamos las fechas para los botones de navegación (semana anterior y siguiente)
    prev_week_date = (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d')
    next_week_date = (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d')

    # Filtrar los horarios que caen exactamente dentro de esta semana y fecha
    horarios_semana = Horario.objects.filter(fecha__range=[start_of_week, end_of_week])

    # Agrupamos por día de la semana
    context = {
        'lunes': horarios_semana.filter(diaSemana__iexact='Lunes'),
        'martes': horarios_semana.filter(diaSemana__iexact='Martes'),
        'miercoles': horarios_semana.filter(diaSemana__iexact='Miércoles'),
        'jueves': horarios_semana.filter(diaSemana__iexact='Jueves'),
        'viernes': horarios_semana.filter(diaSemana__iexact='Viernes'),
        'sabado': horarios_semana.filter(diaSemana__iexact='Sábado'),
        'domingo': horarios_semana.filter(diaSemana__iexact='Domingo'),
        
        # Variables de control para las fechas en las tarjetas y botones de navegación
        'start_of_week': start_of_week,
        'lunes_fecha': start_of_week,
        'martes_fecha': start_of_week + timedelta(days=1),
        'miercoles_fecha': start_of_week + timedelta(days=2),
        'jueves_fecha': start_of_week + timedelta(days=3),
        'viernes_fecha': start_of_week + timedelta(days=4),
        'sabado_fecha': start_of_week + timedelta(days=5),
        'domingo_fecha': start_of_week + timedelta(days=6),
        'prev_week_date': prev_week_date,
        'next_week_date': next_week_date,
    }
    
    return render(request, 'registro_horas/horarios_lista.html', context)
@login_required(login_url='login')
def crear_horario(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha') # Ej: '2026-04-06'
        horaInicio = request.POST.get('horaInicio')
        horaFin = request.POST.get('horaFin')
        capacidadMaxima = request.POST.get('capacidadMaxima')

        if fecha_str:
            # Convertimos el string de la fecha a un objeto datetime
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            # Diccionario para traducir el día de la semana al español
            dias_semana = {
                0: 'Lunes',
                1: 'Martes',
                2: 'Miércoles',
                3: 'Jueves',
                4: 'Viernes',
                5: 'Sábado',
                6: 'Domingo'
            }
            
            # Obtenemos el número del día (0 al 6) y lo mapeamos a texto
            dia_numero = fecha_obj.weekday()
            diaSemana = dias_semana[dia_numero]
        else:
            diaSemana = 'Lunes' # Valor por defecto si por algo estuviera vacío

        # Creamos el registro en MySQL de forma limpia y automática
        Horario.objects.create(
            diaSemana=diaSemana,
            horaInicio=horaInicio,
            horaFin=horaFin,
            capacidadMaxima=capacidadMaxima,
            cuposOcupados=0,
            fecha=fecha_str
        )
        return redirect('registro_horas:lista_horarios')

    return render(request, 'registro_horas/horarios_form.html')

@login_required(login_url='login')
def detalle_horario(request, pk):
    # 1. Obtenemos el horario exacto al que le dio clic el administrador
    horario_seleccionado = get_object_or_404(Horario, pk=pk)
    
    # 2. Buscamos TODOS los horarios que correspondan EXACTAMENTE a la misma fecha 
    # (así si pinchas el martes 7 de abril, solo saldrán los turnos de ese martes 7 de abril)
    if horario_seleccionado.fecha:
        horarios_del_dia = Horario.objects.filter(fecha=horario_seleccionado.fecha)
    else:
        # Por si algún registro antiguo no tuviera fecha, caemos en filtrar por día de semana
        horarios_del_dia = Horario.objects.filter(diaSemana__iexact=horario_seleccionado.diaSemana)
    
    context = {
        'horario_seleccionado': horario_seleccionado,
        'horarios': horarios_del_dia,
    }
    return render(request, 'registro_horas/horarios_detalle.html', context)

@login_required(login_url='login')
def editar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        horaInicio = request.POST.get('horaInicio')
        horaFin = request.POST.get('horaFin')
        capacidadMaxima = request.POST.get('capacidadMaxima')

        if fecha_str:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            dias_semana = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
            diaSemana = dias_semana[fecha_obj.weekday()]
            
            # Actualizamos los campos
            horario.fecha = fecha_str
            horario.diaSemana = diaSemana

        horario.horaInicio = horaInicio
        horario.horaFin = horaFin
        horario.capacidadMaxima = capacidadMaxima
        horario.save()

        # Redirigimos de vuelta a los detalles de ese día
        return redirect('registro_horas:detalle_horario', pk=horario.pk)

    context = {
        'horario': horario
    }
    return render(request, 'registro_horas/horario_editar.html', context)

@login_required(login_url='login')
def eliminar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verificamos si el usuario actual con su contraseña es válido y es staff/superadmin
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None and user.is_staff:
            # Contraseña correcta y permisos de administrador confirmados
            horario.delete()
            return redirect('registro_horas:lista_horarios')
        else:
            # Contraseña incorrecta o sin permisos: puedes redirigir con un mensaje o volver al detalle
            # (Opcional: puedes pasar un parámetro de error en la URL para mostrar una alerta)
            return redirect('registro_horas:detalle_horario', pk=pk)
            
    return redirect('registro_horas:detalle_horario', pk=pk)