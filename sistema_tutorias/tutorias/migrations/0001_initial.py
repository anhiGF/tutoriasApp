# Generated by Django 5.2 on 2025-05-27 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('num_control', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('correo_electronico', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('semestre', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('fecha_nac', models.DateField(blank=True, null=True)),
                ('tipo_usuario', models.CharField(choices=[('Estudiante', 'Estudiante'), ('Tutor', 'Tutor'), ('Administrador', 'Administrador')], max_length=15)),
                ('fecha_registro', models.DateField()),
                ('ultima_sesion', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecuperacionContraseña',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tutorias.usuario')),
                ('token', models.CharField(max_length=64)),
                ('expira_en', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField()),
                ('id_destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_recibidos', to='tutorias.usuario')),
                ('id_remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_enviados', to='tutorias.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id_tutoria', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('duracion', models.IntegerField()),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')], max_length=15)),
                ('id_estudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorias_como_estudiante', to='tutorias.usuario')),
                ('id_tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorias_como_tutor', to='tutorias.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id_recurso', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('Documento', 'Documento'), ('Enlace', 'Enlace'), ('Video', 'Video')], max_length=10)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('id_tutoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.tutoria')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialModificaciones',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('accion', models.CharField(max_length=50)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorias.usuario')),
                ('id_tutoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.tutoria')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id_feedback', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.usuario')),
                ('id_tutoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.tutoria')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id_evaluacion', models.AutoField(primary_key=True, serialize=False)),
                ('puntaje', models.PositiveSmallIntegerField()),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('id_tutoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.tutoria')),
            ],
        ),
    ]
