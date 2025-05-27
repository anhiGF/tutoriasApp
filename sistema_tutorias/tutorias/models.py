from django.db import models

class Usuario(models.Model):
    num_control = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    semestre = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_nac = models.DateField(null=True, blank=True)
    
    TIPO_USUARIO = [
        ('Estudiante', 'Estudiante'),
        ('Tutor', 'Tutor'),
        ('Administrador', 'Administrador'),
    ]
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO)
    fecha_registro = models.DateField()
    ultima_sesion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.num_control})"


class RecuperacionContraseña(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=64)
    expira_en = models.DateTimeField()


class Tutoria(models.Model):
    ESTADO = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    id_tutoria = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.IntegerField()
    estado = models.CharField(max_length=15, choices=ESTADO)
    id_tutor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tutorias_como_tutor', null=True, blank=True)
    id_estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tutorias_como_estudiante', null=True, blank=True)


class HistorialModificaciones(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField()
    id_remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    id_destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')


class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    puntaje = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    id_tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)


class Recurso(models.Model):
    TIPO_RECURSO = [
        ('Documento', 'Documento'),
        ('Enlace', 'Enlace'),
        ('Video', 'Video'),
    ]
    id_recurso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_RECURSO)
    descripcion = models.TextField(blank=True, null=True)
    url = models.URLField()
    id_tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)


class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    comentario = models.TextField()
    fecha = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
