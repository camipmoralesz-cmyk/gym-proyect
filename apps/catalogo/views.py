from django.shortcuts import render

def lista_maquinas_admin(request):
    return render(request, 'catalogo/catalogo_maquinas_adm.html')

def crear_maquina(request):
    return render(request, 'catalogo/catalogo_form.html')

def editar_maquina(request, pk=1):
    return render(request, 'catalogo/catalogo_editar.html')

# Vista del catálogo para el cliente
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
    return render(request, 'catalogo/catalogo_maquinas.html', {'maquinas': maquinas})