from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import RegistroForm, UsuarioAdminForm, UsuarioEditarForm
from .models import Perfil, Cliente, Administrador


def es_staff(user):
    return user.is_staff


# ---------- Login lo hace LoginView de Django (ver urls.py) ----------

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


def registro_view(request):
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            user = form.save()
            Cliente.objects.create(idUsuario=user)   # quien se registra es cliente
        login(request, user)
        messages.success(request, '¡Cuenta creada!')
        return redirect('usuarios:perfil')
    return render(request, 'usuarios/registro.html', {'form': form})  # tu template actual


@login_required
def perfil_view(request):
    # En el template usa {{ user.get_full_name }}, {{ user.email }}, {{ user.perfil.rut }}
    return render(request, 'usuarios/perfil.html')


# ============================================================
# HITO 1 + 2: lista + buscador de CLIENTES
# ============================================================
@login_required
@user_passes_test(es_staff, login_url='usuarios:login')
def gestion_usuarios_view(request):
    q = request.GET.get('q', '').strip()

    usuarios = User.objects.select_related('cliente', 'administrador', 'perfil') \
                           .order_by('first_name', 'last_name')
    if q:
        usuarios = usuarios.filter(cliente__isnull=False).filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(perfil__rut__icontains=q)
        )
    return render(request, 'usuarios/gestion_usuarios.html',
                  {'usuarios': usuarios, 'q': q, 'hoy': date.today()})


# ============================================================
# HITO 3: crear
# ============================================================
@login_required
@user_passes_test(es_staff, login_url='usuarios:login')
def crear_usuario_view(request):
    form = UsuarioAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            user = form.save()
            if form.cleaned_data['rol'] == 'administrador':
                user.is_staff = True          # esto le da acceso a la gestión
                user.save()
                Administrador.objects.create(
                    idUsuario=user, nivelPermiso=form.cleaned_data['nivelPermiso'])
            else:
                Cliente.objects.create(
                    idUsuario=user,
                    fechaVencimientoMembrecia=form.cleaned_data['fechaVencimientoMembrecia'])
        messages.success(request, f"Usuario '{user.get_full_name()}' creado.")
        return redirect('usuarios:gestion_usuarios')
    return render(request, 'usuarios/usuario_form.html', {'form': form})


# ============================================================
# HITO 4: editar (patrón figura_editar)
# ============================================================
@login_required
@user_passes_test(es_staff, login_url='usuarios:login')
def editar_usuario_view(request, id):
    usuario = get_object_or_404(User, pk=id)
    admin = Administrador.objects.filter(idUsuario=usuario).first()
    cliente = Cliente.objects.filter(idUsuario=usuario).first()   # NUEVO
    perfil = getattr(usuario, 'perfil', None)

    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario, es_admin=admin is not None)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.username = user.email
                user.save()
                Perfil.objects.update_or_create(user=user, defaults={
                    'rut': form.cleaned_data['rut'],
                    'telefono': form.cleaned_data['telefono']})
                if admin:
                    admin.nivelPermiso = form.cleaned_data['nivelPermiso']
                    admin.save()
                if cliente:   # NUEVO: guarda la fecha de membresía
                    cliente.fechaVencimientoMembrecia = form.cleaned_data['fechaVencimientoMembrecia']
                    cliente.save()
            messages.success(request, f"Usuario '{user.get_full_name()}' actualizado.")
            return redirect('usuarios:gestion_usuarios')
    else:
        form = UsuarioEditarForm(instance=usuario, es_admin=admin is not None, initial={
            'rut': perfil.rut if perfil else '',
            'telefono': perfil.telefono if perfil else '',
            'nivelPermiso': admin.nivelPermiso if admin else '',
            'fechaVencimientoMembrecia': cliente.fechaVencimientoMembrecia if cliente else None})

    return render(request, 'usuarios/usuario_editar.html', {
        'form': form, 'usuario': usuario,
        'titulo_accion': 'Editar Usuario', 'boton_texto': 'Actualizar'})


# ============================================================
# HITO 5a: eliminar con confirmación (figura_eliminar)
# ============================================================
@login_required
@user_passes_test(es_staff, login_url='usuarios:login')
def eliminar_usuario_view(request, id):
    usuario = get_object_or_404(User, pk=id)

    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('usuarios:gestion_usuarios')

    if request.method == 'POST':
        nombre = usuario.get_full_name()
        usuario.delete()       # CASCADE borra Perfil, Cliente/Administrador y datos hijos
        messages.success(request, f"Usuario '{nombre}' eliminado.")
        return redirect('usuarios:gestion_usuarios')

    return render(request, 'usuarios/usuario_confirmar_eliminar.html', {'usuario': usuario})


# ============================================================
# HITO 5b: activar / desactivar cliente (baja lógica)
# is_active es un campo propio de Django: si es False, no puede iniciar sesión.
# ============================================================
@login_required
@user_passes_test(es_staff, login_url='usuarios:login')
@require_POST
def cambiar_estado_cliente_view(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.estado = 'desactivado' if cliente.estado == 'activo' else 'activo'
    cliente.save()
    cliente.idUsuario.is_active = (cliente.estado == 'activo')
    cliente.idUsuario.save()
    messages.success(request, f"Cliente '{cliente.idUsuario.get_full_name()}': {cliente.get_estado_display()}.")
    return redirect('usuarios:gestion_usuarios')