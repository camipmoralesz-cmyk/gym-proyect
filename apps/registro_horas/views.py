from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Horario, Reserva


#-------------------------------
# PANTALLA PRINCIPAL (ADMIN - LISTA DE HORARIOS)
#-------------------------------
@login_required(login_url='login')
def lista_horarios(request):
    fecha_param = request.GET.get('fecha')
    
    if fecha_param:
        try:
            ref_date = datetime.strptime(fecha_param, '%Y-%m-%d').date()
        except ValueError:
            ref_date = datetime.now().date()
    else:
        ref_date = datetime.now().date()

    start_of_week = ref_date - timedelta(days=ref_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    prev_week_date = (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d')
    next_week_date = (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d')

    horarios_semana = Horario.objects.filter(fecha__range=[start_of_week, end_of_week])

    context = {
        'lunes': horarios_semana.filter(diaSemana__iexact='Lunes'),
        'martes': horarios_semana.filter(diaSemana__iexact='Martes'),
        'miercoles': horarios_semana.filter(diaSemana__iexact='Miércoles'),
        'jueves': horarios_semana.filter(diaSemana__iexact='Jueves'),
        'viernes': horarios_semana.filter(diaSemana__iexact='Viernes'),
        'sabado': horarios_semana.filter(diaSemana__iexact='Sábado'),
        'domingo': horarios_semana.filter(diaSemana__iexact='Domingo'),
        
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


#-------------------------------
# CREAR HORARIOS
#-------------------------------
@login_required(login_url='login')
def crear_horario(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        horaInicio = request.POST.get('horaInicio')
        horaFin = request.POST.get('horaFin')
        capacidadMaxima = request.POST.get('capacidadMaxima')

        if fecha_str:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            dias_semana = {
                0: 'Lunes',
                1: 'Martes',
                2: 'Miércoles',
                3: 'Jueves',
                4: 'Viernes',
                5: 'Sábado',
                6: 'Domingo'
            }
            diaSemana = dias_semana[fecha_obj.weekday()]
        else:
            diaSemana = 'Lunes'

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


#-------------------------------
# DETALLES DE LOS HORARIOS
#-------------------------------
@login_required(login_url='login')
def detalle_horario(request, pk):
    horario_seleccionado = get_object_or_404(Horario, pk=pk)
    
    if horario_seleccionado.fecha:
        horarios_del_dia = Horario.objects.filter(fecha=horario_seleccionado.fecha)
    else:
        horarios_del_dia = Horario.objects.filter(diaSemana__iexact=horario_seleccionado.diaSemana)
    
    context = {
        'horario_seleccionado': horario_seleccionado,
        'horarios': horarios_del_dia,
    }
    return render(request, 'registro_horas/horarios_detalle.html', context)


#-------------------------------
# EDITAR UN HORARIO
#-------------------------------
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
            
            horario.fecha = fecha_str
            horario.diaSemana = diaSemana

        horario.horaInicio = horaInicio
        horario.horaFin = horaFin
        horario.capacidadMaxima = capacidadMaxima
        horario.save()

        return redirect('registro_horas:detalle_horario', pk=horario.pk)

    context = {
        'horario': horario
    }
    return render(request, 'registro_horas/horario_editar.html', context)


#-------------------------------
# ELIMINAR HORARIO
#-------------------------------
@login_required(login_url='login')
def eliminar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None and user.is_staff:
            horario.delete()
            return redirect('registro_horas:lista_horarios')
        else:
            return redirect('registro_horas:detalle_horario', pk=pk)
            
    return redirect('registro_horas:detalle_horario', pk=pk)


#-------------------------------
# VISTA DEL CLIENTE (HORARIOS Y RESERVAS)
#-------------------------------
@login_required
def horarios_view(request):
    fecha_param = request.GET.get('fecha')
    
    if fecha_param:
        try:
            ref_date = datetime.strptime(fecha_param, '%Y-%m-%d').date()
        except ValueError:
            ref_date = datetime.now().date()
    else:
        ref_date = datetime.now().date()

    start_of_week = ref_date - timedelta(days=ref_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    prev_week_date = (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d')
    next_week_date = (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d')

    horarios_semana = Horario.objects.filter(fecha__range=[start_of_week, end_of_week])

    context = {
        'lunes': horarios_semana.filter(diaSemana__iexact='Lunes'),
        'martes': horarios_semana.filter(diaSemana__iexact='Martes'),
        'miercoles': horarios_semana.filter(diaSemana__iexact='Miércoles'),
        'jueves': horarios_semana.filter(diaSemana__iexact='Jueves'),
        'viernes': horarios_semana.filter(diaSemana__iexact='Viernes'),
        'sabado': horarios_semana.filter(diaSemana__iexact='Sábado'),
        'domingo': horarios_semana.filter(diaSemana__iexact='Domingo'),
        
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
    
    return render(request, 'registro_horas/horarios.html', context)


@login_required
def realizar_reserva(request, bloque_id):
    Reserva.objects.get_or_create(
        usuario=request.user,
        bloque_horario=bloque_id
    )
    return redirect('registro_horas:horarios')