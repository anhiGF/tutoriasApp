from django.apps import AppConfig
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class TutoriasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorias'

    def ready(self):
        from .models import Usuario
        from django.db.utils import OperationalError, ProgrammingError
        import datetime

        try:
            if not Usuario.objects.filter(tipo_usuario='Administrador').exists():
                Usuario.objects.create(
                    num_control=1,
                    nombre='Admin',
                    primer_apellido='General',
                    segundo_apellido='',
                    correo_electronico='admin@tutorias.com',
                    contraseña=make_password('admin123'),
                    tipo_usuario='Administrador',
                    semestre=None,
                    fecha_nac=datetime.date(1990, 1, 1),
                    fecha_registro=timezone.now().date(),
                    ultima_sesion=None,
                )
                print("✅ Usuario administrador creado automáticamente.")
        except (OperationalError, ProgrammingError):
            # Esto evita errores si la tabla aún no está migrada
            pass