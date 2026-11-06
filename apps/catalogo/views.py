from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Maquina
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404

# LISTA DE TODAS MLAS MAQUINAS
def lista_maquinas_admin(request):
    maquinas = Maquina.objects.all()
    context = {
        'maquinas': maquinas
    }
    return render(request, 'catalogo/catalogo_maquinas.html', context)

#CREAR UNA MAQUINA NUEVA
@login_required(login_url='login')
def crear_maquina(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        instruccionesUso = request.POST.get('instruccionesUso')
        estado_str = request.POST.get('estadoDisponible')
        estadoDisponible = True if estado_str == 'True' else False
        
        # Procesamiento real del archivo de imagen
        imagen_url = ''
        if request.FILES.get('imagen'):
            imagen_archivo = request.FILES['imagen']
            fs = FileSystemStorage()
            filename = fs.save(f"maquinas/{imagen_archivo.name}", imagen_archivo)
            imagen_url = fs.url(filename) # Guarda la ruta ej: /media/maquinas/foto.jpg

        # Creamos y guardamos el registro en la base de datos MySQL
        Maquina.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            instruccionesUso=instruccionesUso,
            estadoDisponible=estadoDisponible,
            imagen=imagen_url,
            idAdministrador=request.user # Asocia la máquina al administrador autenticado actualmente
        )
        
        # Redirige de regreso al catálogo general para ver la nueva máquina añadida
        return redirect('catalogo:gestion_maquinas')

    return render(request, 'catalogo/catalogo_form.html')

#EDITAR UNA MAQUINA
@login_required(login_url='login')
def editar_maquina(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    
    if request.method == 'POST':
        maquina.nombre = request.POST.get('nombre')
        maquina.descripcion = request.POST.get('descripcion')
        maquina.instruccionesUso = request.POST.get('instruccionesUso')
        maquina.estadoDisponible = True if request.POST.get('estadoDisponible') == 'True' else False
        
        # Si marcaron la casilla de eliminar imagen
        if request.POST.get('eliminar_imagen'):
            maquina.imagen = ''
        
        # Si suben una nueva imagen
        elif request.FILES.get('imagen'):
            imagen_archivo = request.FILES['imagen']
            fs = FileSystemStorage()
            filename = fs.save(f"maquinas/{imagen_archivo.name}", imagen_archivo)
            maquina.imagen = fs.url(filename)
            
        maquina.save()
        return redirect('catalogo:gestion_maquinas')

    context = {
        'maquina': maquina
    }
    return render(request, 'catalogo/catalogo_editar.html', context)

#ELIMINAR UNA MAQUINA
@login_required(login_url='login')
def eliminar_maquina(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        password = request.POST.get('password')
        # Verificamos si la contraseña coincide con la del usuario administrador actual
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            maquina.delete()
            return redirect('catalogo:gestion_maquinas')
        else:
            # Si la contraseña es incorrecta, puedes redirigir o mostrar un aviso
            return redirect('catalogo:gestion_maquinas')
            
    return redirect('catalogo:gestion_maquinas')