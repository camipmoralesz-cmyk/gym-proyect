from django.shortcuts import render
#from django.contrib.auth.decorators import login_required

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
#ME PIDE CAMBIAR ESTA LINEA PARA QUE MUESTRE MI PAGINA QUE YO CREE ASI ESTABA LA LINEA ACTUAL
    #return render(request, 'registro_horas/horarios_lista.html') actual
    #return render(request, 'registro_horas/horarios.html')modificada

#  NUEVA VISTA PARA EL CATÁLOGO DE MÁQUINAS DEL CLIENTE

def catalogo_maquinas_view(request):
    maquinas = [
        {
            'nombre': 'Caminadora Pro Treadmill',
            'categoria': 'Cardio',
            'estado': 'Disponible',
            'descripcion': 'Cinta de correr profesional con ajuste de inclinación digital y monitor cardíaco.',
            'imagen': 'img/caminadora.jpg'
        },
        {
            'nombre': 'Bicicleta Estática Retro',
            'categoria': 'Cardio',
            'estado': 'Disponible',
            'descripcion': 'Bicicleta fija de alta resistencia con pantalla de control de velocidad y tiempo.',
            'imagen': 'img/bicicleta.jpg'
        },
        {
            'nombre': 'Multiestación de Poleas',
            'categoria': 'Fuerza / Sobrecarga',
            'estado': 'En Mantención',
            'descripcion': 'Torre de poleas cruzadas para entrenamiento funcional y musculación completa.',
            'imagen': 'img/poleas.jpg'
        },
        {
            'nombre': 'Prensa de Piernas 45°',
            'categoria': 'Tren Inferior',
            'estado': 'Disponible',
            'descripcion': 'Máquina inclinada para desarrollo de cuádriceps, glúteos y pantorrillas con seguro ajustable.',
            'imagen': 'img/prensa.jpg'
        },
    ]
    return render(request, 'registro_horas/catalogo_maquinas.html', {'maquinas': maquinas})