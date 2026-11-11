# Sistema de Gestión Integral para Gimnasio (Fitness Retro)

## Plataforma web colaborativa desarrollada en Django y MySQL para la administración, supervisión operativa y reserva de espacios en un centro de entrenamiento físico. El sistema permite gestionar perfiles de usuarios, un catálogo interactivo de maquinaria y la planificación/reserva de bloques horarios con aforos controlados.

## Ficha Técnica del Proyecto

# Plataforma / Negocio: Fitness Retro (Gimnasio y Centro de Entrenamiento)

# Framework Backend: Django (Python)
# Base de Datos: MySQL
# Frontend y Estilos: Bootstrap 5, HTML5, CSS3
# Entidad de Contexto / Agrupación (ORM): "User" / "Administrador" (Control de roles, permisos y supervisión de recursos)
# Entidad Principal Gestionable (ORM): "Maquina" / "Horario" (Núcleo central de datos sobre el cual operan las acciones del sistema: CRUD completo)
# Propósito de la Sesión ("request.session"): Planificador de horarios y gestión de cupos/reservas activas de los clientes en tiempo real.

## Integrantes del Equipo
# Camila Morales 
# Jessica Pacheco
# Marian Paraguan

# Guía de Instalación y Configuración Paso a Paso

# 1. Clonar el Repositorio

# 2. Crear, Activar e Instalar dependencias del Entorno Virtual:

# 3. Configurar la Base de Datos (MySQL): Primero, se debe crear el archivo .env y copiar ahi los datos de la conexión. Segundo, ejecutar pip install pymysql en la terminal. Tercero, ejecutar python manage.py check --database default para verificar que se pudo hacer la conexion. Y cuarto, ejecutar python manage.py migrate para hacer las migraciones

# 4. Iniciar el Servidor de Desarrollo

# Credenciales de Acceso

## Para acceder al sistema primero debemos crear un super admin, para eso, se debe ejecutar python manage.py createsuperuser. De esta forma al querer iniciar sesión con ese usuario, lo guiará al panel administrativo.

# En cambio, para acceder como cliente, se debe crear un n uevo usuario desde el "admin, colocando /admin en la ruta (http://127.0.0.1:8000/admin/), en donde se inicia con la cuenta de super usuario. Una vez creado el usuario cliente, puede ingresar esas credenciales y lo guiará al panel del cliente.

# Bitácora de Uso Técnico y Ético de Inteligencia Artificial

## Durante la fase de integración, unificación de código y resolución de conflictos del proyecto, se utilizó Inteligencia Artificial como herramienta de asistencia técnica. A continuación se documentan 3 prompts clave en las áreas de Arquitectura, ORM y Seguridad, junto con su correspondiente evaluación crítica y adaptación.

## Prompt 1: Arquitectura y Estructura Modular

### Área: Arquitectura de Software

### Prompt Utilizado:
### "Actúa como un arquitecto senior en Django. Necesito estructurar un proyecto multi-app que divida la lógica en las aplicaciones 'core', 'catalogo', 'usuarios' y 'registro_horas'. ¿Cómo debo configurar las rutas principales en urls.py, la carga de archivos multimedia en modo DEBUG y la separación de vistas para evitar colisiones de plantillas entre el perfil admin y cliente?"

### Respuesta de la IA:
### Propuso un esquema de enrutamiento principal mediante include('apps.nombre.urls'), el manejo explícito de static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) al final de urlpatterns, y la organización estricta de plantillas en subcarpetas templates/nombre_app/.

### Justificación Crítica y Adaptación:
### La solución fue adaptada integrando las rutas con espacios de nombres (app_name = 'catalogo'), lo que permitió resolver los conflictos de fusión entre la rama main y ramaJessica. Esto evitó redundancias en los nombres de las plantillas de login y dashboard, garantizando una separación limpia entre la vista administrativa y el portal del cliente.

## Prompt 2: Configuración de Modelos y Mapeo ORM MySQL

### Área: Base de Datos y ORM

### Prompt Utilizado:
### "Tengo un modelo 'Maquina' y un modelo 'Horario' en Django que deben vincularse con tablas ya existentes en MySQL ('Maquina' y 'horario'). ¿Cómo defino correctamente los atributos en models.py usando la clave foránea hacia settings.AUTH_USER_MODEL, asegurando tipos de datos exactos, métodos str y la especificación de db_table sin perder los campos de imagen?"

### Respuesta de la IA:
### Proporcionó las clases de modelos heredando de models.Model, haciendo uso de settings.AUTH_USER_MODEL para el campo idAdministrador, declarando la subclase Meta con db_table = 'Maquina', e incluyendo el manejo de imágenes mediante un campo de texto/ruta junto al método __str__.

### Justificación Crítica y Adaptación:
### Se aceptó el uso de settings.AUTH_USER_MODEL por ser la mejor práctica en Django en lugar de importar User directamente. Se preservaron los campos personalizados desarrollados previamente en la base de datos (como instruccionesUso y estadoDisponible) y se ajustó la propiedad @property cupos_disponibles con la función max(0, Capacidad - Ocupados) para evitar valores negativos en el portal de cliente.

## Prompt 3: Seguridad, Autenticación y Control de Accesos

### Área: Seguridad y Control de Acceso

### Prompt Utilizado:

### "¿Cuál es la forma más segura en Django para implementar un login unificado que diferencie a los administradores de los clientes, y cómo puedo proteger las vistas del dashboard para que un usuario estándar no pueda acceder ni modificar máquinas u horarios, incluso introduciendo la URL directamente?"

### Respuesta de la IA:
### Recomendó una lógica centralizada en login_view que evalúa user.is_staff o user.is_superuser para decidir la redirección (hacia core:dashboard o registro_horas:horarios), acompañada del decorador @login_required y una verificación interna de permisos en cada vista sensible que cierra la sesión si el acceso es indebido.

### Justificación Crítica y Adaptación:
### Se adaptó la vista de inicio de sesión para consolidar en una sola función login_view los intentos de login tanto de la administración como de los clientes, eliminando vistas redundantes. Se añadió la verificación de contraseña del administrador en las acciones destructivas de la aplicación (como eliminar máquinas o borrar horarios) para brindar una capa adicional de confirmación antes de impactar la base de datos MySQL.