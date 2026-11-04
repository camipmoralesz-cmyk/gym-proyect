from django.shortcuts import render

def lista_maquinas_admin(request):
    # Vista estática temporal orientada exclusivamente a la interfaz visual
    return render(request, 'catalogo/catalogo_maquinas_adm.html')

def crear_maquina(request):
    # Vista visual para el formulario de creación de máquinas
    return render(request, 'catalogo/catalogo_form.html')

def editar_maquina(request, pk=1):
    # Vista visual temporal para editar una máquina existente
    return render(request, 'catalogo/catalogo_editar.html')