// static/js/funciones.js

function haySeleccion() {
    const checks = document.querySelectorAll('.chk-horario');
    return Array.from(checks).some(chk => chk.checked);
}

function mostrarAlerta() {
    const alerta = document.getElementById('alertaSeleccion');
    if (alerta) {
        alerta.classList.remove('d-none');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function cerrarAlerta() {
    const alerta = document.getElementById('alertaSeleccion');
    if (alerta) {
        alerta.classList.add('d-none');
    }
}

function validarEditar(btn) {
    if (haySeleccion()) {
        cerrarAlerta();
        // Leemos la URL directamente del atributo data-url del botón
        const urlEdicion = btn.getAttribute('data-url');
        window.location.href = urlEdicion;
    } else {
        mostrarAlerta();
    }
}

function validarEliminar() {
    if (haySeleccion()) {
        cerrarAlerta();
        const modalEl = document.getElementById('modalEliminarHorario');
        if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    } else {
        mostrarAlerta();
    }
}