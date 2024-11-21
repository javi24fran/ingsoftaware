from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ingApp. models import Alumno

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Proporcione un nombre de usuario y una contraseña válida.",
    }
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'etnia', 'numero_emergencia', 'colegio_procedencia', 'beneficio_junaeb', 'sistema_salud']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellido'}),
            'numero_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese número de emergencia'}),
            'colegio_procedencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el colegio de procedencia'}),
            'etnia': forms.Select(attrs={'class': 'form-control'}),
            'beneficio_junaeb': forms.Select(attrs={'class': 'form-control'}),
            'sistema_salud': forms.Select(attrs={'class': 'form-control'}),
        }
    
    # Validaciones adicionales si se necesitan
    def clean_numero_emergencia(self):
        numero_emergencia = self.cleaned_data.get('numero_emergencia')
        if not numero_emergencia.isdigit():
            raise forms.ValidationError('El número de emergencia debe contener solo números.')
        return numero_emergencia