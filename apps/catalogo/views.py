from django.shortcuts import render
from .models import Maquina

def lista_maquinas_admin(request):
    return render(request, 'catalogo/catalogo_maquinas_adm.html')

def crear_maquina(request):
    return render(request, 'catalogo/catalogo_form.html')

def editar_maquina(request, pk=1):
    return render(request, 'catalogo/catalogo_editar.html')

# Vista del catálogo para el cliente
def catalogo_maquinas_view(request):
    # Reemplazamos la lista estática por los datos reales de la base de datos
    maquinas = Maquina.objects.all()
    
    context = {
        'maquinas': maquinas
    }
    # Respetamos exactamente el return render con el template que ella diseñó
    return render(request, 'catalogo/catalogo_maquinas.html', context)