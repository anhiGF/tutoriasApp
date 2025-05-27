from django.db import IntegrityError
import requests
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from datetime import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render

from tutorias.forms import RegistroUsuarioForm
from tutorias.models import Usuario, RecuperacionContraseña

def index(request):
    return render(request, 'index.html')

def login_modal(request):
    return render(request, 'modals/login.html')

def altas_modal(request):
    return render(request, 'modals/altas.html')

def recuperar_password_modal(request):
    return render(request, 'modals/recuperacion_contraseña.html')

def login_view(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('correo_electronico')
        password = request.POST.get('contraseña')
        captcha_response = request.POST.get('g-recaptcha-response')

        # Validación de CAPTCHA (opcional)
        # Puedes descomentar esto si ya tienes reCAPTCHA activo:
        # import requests
        # recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        # secret_key = 'TU_SECRET_KEY'
        # recaptcha_result = requests.post(recaptcha_url, data={
        #     'secret': secret_key,
        #     'response': captcha_response
        # }).json()
        # if not recaptcha_result.get('success'):
        #     messages.error(request, 'Por favor verifica el CAPTCHA.')
        #     return redirect('index')

        try:
            user = Usuario.objects.get(correo_electronico=email)

            if check_password(password, user.contraseña):
                request.session['num_control'] = user.num_control
                request.session['nombre'] = user.nombre
                request.session['tipo_usuario'] = user.tipo_usuario

                # Guardar la fecha de última sesión
                user.ultima_sesion = timezone.now()
                user.save()

                if user.tipo_usuario == 'Tutor':
                    return redirect('panel_tutor')
                elif user.tipo_usuario == 'Estudiante':
                    return redirect('gestion_tutorias')
                elif user.tipo_usuario == 'Administrador':
                    return redirect('admin_panel')
            else:
                messages.error(request, 'Contraseña incorrecta.')
                return redirect('index')

        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
            return redirect('index')

    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')  

def reset_password_view(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        nueva_contraseña = request.POST.get('nueva_contraseña')
        
        try:
            recuperacion = RecuperacionContraseña.objects.get(token=token, expira_en__gt=timezone.now())
            usuario = Usuario.objects.get(num_control=recuperacion.num_control)
            usuario.contraseña = make_password(nueva_contraseña)
            usuario.save()

            recuperacion.delete()
            return render(request, 'modals/mensaje.html', {'mensaje': 'Contraseña restablecida con éxito. Ya puedes iniciar sesión.'})
        except RecuperacionContraseña.DoesNotExist:
            return render(request, 'modals/mensaje.html', {'mensaje': 'El enlace de recuperación es inválido o ha expirado.'})

    elif request.method == 'GET' and 'token' in request.GET:
        token = request.GET.get('token')
        return render(request, 'pages/restablecer_contraseña.html', {'token': token})
    else:
        return render(request, 'modals/mensaje.html', {'mensaje': 'Token no proporcionado.'})
    
def send_reset_email_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo_electronico')
        try:
            usuario = Usuario.objects.get(correo_electronico=correo)
            token = get_random_string(length=32)
            expira_en = timezone.now() + timezone.timedelta(hours=1)

            RecuperacionContraseña.objects.update_or_create(
                num_control=usuario.num_control,
                defaults={'token': token, 'expira_en': expira_en}
            )

            enlace = request.build_absolute_uri(f"/restablecer_contraseña/?token={token}")
            asunto = 'Recuperación de contraseña - ITSJ'
            mensaje = f"Hola,\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n{enlace}\n\nEste enlace expirará en 1 hora."

            send_mail(
                asunto,
                mensaje,
                'naniflores1509@gmail.com',
                [correo],
                fail_silently=False,
            )

            return render(request, 'modals/mensaje.html', {'mensaje': 'Correo de recuperación enviado. Revisa tu bandeja de entrada.'})
        except Usuario.DoesNotExist:
            return render(request, 'modals/mensaje.html', {'mensaje': 'No se encontró una cuenta con ese correo electrónico.'})
    else:
        return render(request, 'modals/recuperar_contraseña.html')
    
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Usuario
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.fecha_registro = timezone.now().date()
            usuario.save()
            return redirect('login')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def altas_modal2(request):
    errores = []
    data = {}

    if request.method == 'POST':
        data = {
            'num_control': request.POST.get('num_control'),
            'nombre': request.POST.get('nombre'),
            'primer_apellido': request.POST.get('primer_apellido'),
            'segundo_apellido': request.POST.get('segundo_apellido'),
            'correo_electronico': request.POST.get('correo_electronico'),
            'contraseña': request.POST.get('contraseña'),
            'confirmar_contraseña': request.POST.get('confirmar_contraseña'),
            'semestre': request.POST.get('semestre'),
            'fecha_nac': request.POST.get('fecha_nac'),
            'tipo_usuario': request.POST.get('tipo_usuario'),
        }

        # Validaciones
        if Usuario.objects.filter(num_control=data['num_control']).exists():
            errores.append("Ya existe un usuario con ese número de control.")
        if Usuario.objects.filter(correo_electronico=data['correo_electronico']).exists():
            errores.append("Ya existe un usuario con ese correo.")
        if data['contraseña'] != data['confirmar_contraseña']:
            errores.append("Las contraseñas no coinciden.")

        if not errores:
            try:
                nuevo = Usuario(
                    num_control=data['num_control'],
                    nombre=data['nombre'],
                    primer_apellido=data['primer_apellido'],
                    segundo_apellido=data['segundo_apellido'],
                    correo_electronico=data['correo_electronico'],
                    contraseña=make_password(data['contraseña']),
                    semestre=data['semestre'] if data['semestre'] else None,
                    fecha_nac=data['fecha_nac'] if data['fecha_nac'] else None,
                    tipo_usuario=data['tipo_usuario']
                )
                nuevo.save()
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('index')
            except IntegrityError:
                errores.append("Error al guardar el usuario.")
    
    return render(request, 'modals/altas_modal.html', {'errores': errores, 'data': data})