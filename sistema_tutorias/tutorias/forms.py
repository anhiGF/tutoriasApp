from django import forms
from .models import Usuario
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegistroUsuarioForm(forms.ModelForm):
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = [
            'num_control', 'nombre', 'primer_apellido', 'segundo_apellido',
            'correo_electronico', 'contraseña', 'semestre', 'fecha_nac', 'tipo_usuario'
        ]
        widgets = {
            'contraseña': forms.PasswordInput(),
            'fecha_nac': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_num_control(self):
        num_control = self.cleaned_data.get('num_control')
        if not re.fullmatch(r'\d{8,9}', num_control):
            raise ValidationError("El número de control debe contener entre 8 y 9 dígitos numéricos.")
        if Usuario.objects.filter(num_control=num_control).exists():
            raise ValidationError("Ya existe un perfil para ese número de control.")
        return num_control

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+', nombre):
            raise ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_primer_apellido(self):
        primer_apellido = self.cleaned_data.get('primer_apellido')
        if not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+', primer_apellido):
            raise ValidationError("El primer apellido solo puede contener letras y espacios.")
        return primer_apellido

    def clean_segundo_apellido(self):
        segundo_apellido = self.cleaned_data.get('segundo_apellido')
        if segundo_apellido and not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+', segundo_apellido):
            raise ValidationError("El segundo apellido solo puede contener letras y espacios.")
        return segundo_apellido

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError("El correo electrónico no es válido.")
        if Usuario.objects.filter(correo_electronico=correo).exists():
            raise ValidationError("Ya existe un perfil para ese correo.")
        return correo

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', contraseña):
            raise ValidationError("La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una minúscula y un número.")
        return contraseña

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar = cleaned_data.get('confirmar_contraseña')
        if contraseña and confirmar and contraseña != confirmar:
            self.add_error('confirmar_contraseña', "Las contraseñas no coinciden.")

        semestre = cleaned_data.get('semestre')
        if semestre is not None and semestre <= 0:
            self.add_error('semestre', "El semestre debe ser un número positivo.")
