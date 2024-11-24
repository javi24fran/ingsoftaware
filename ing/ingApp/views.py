from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from ingApp.forms import AlumnoForm, ApoderadoForm
from ingApp.models import Alumno, Apoderado
from django.db import transaction

@login_required
def index(request):
    return render(request, 'ingApp/index.html')


@login_required
def matricula_view(request):
    alumno_form = AlumnoForm(request.POST or None)
    apoderado_form = ApoderadoForm(request.POST or None)

    if request.method == 'POST' and 'form_alumno' in request.POST:
        if alumno_form.is_valid():
            alumno_data = alumno_form.cleaned_data
            alumno_data['fecha_nacimiento'] = alumno_data['fecha_nacimiento'].isoformat()
            request.session['alumno_data'] = alumno_data

            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'alumno_form': alumno_form,
                'apoderado_form': ApoderadoForm(),  # Inicializamos el formulario de apoderado vacío
                'show_apoderado_form': True,  # Mostrar formulario de apoderado
                'show_alumno_form': False,    # Ocultar formulario de alumno
            })
        else:
            # Si el formulario de alumno no es válido
            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'alumno_form': alumno_form,
                'apoderado_form': apoderado_form,
                'show_apoderado_form': False,  # No mostrar formulario de apoderado
                'show_alumno_form': True,     # Mostrar formulario de alumno (no válido)
            })

    # Si el formulario de apoderado fue enviado
    elif request.method == 'POST' and 'form_apoderado' in request.POST:
        apoderado_form = ApoderadoForm(request.POST)

        if apoderado_form.is_valid() and 'alumno_data' in request.session:
            # Guardar los datos del apoderado en la base de datos
            with transaction.atomic():
                # Crear un nuevo alumno con los datos de la sesión
                alumno_data = request.session['alumno_data']
                alumno = Alumno.objects.create(**alumno_data)

                # Crear un apoderado y asociarlo al alumno
                apoderado = apoderado_form.save(commit=False)
                apoderado.alumno = alumno  # Asociamos el apoderado con el alumno
                apoderado.save()

                # Ahora asociamos el apoderado con el alumno en la relación inversa
                alumno.apoderado = apoderado
                alumno.save()

                # Borrar los datos de la sesión después de registrarlos
                del request.session['alumno_data']

            # Redirigir a la página de éxito
            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'apoderado_form': apoderado_form,
                'show_apoderado_form': False,
                'show_alumno_form': False,
                'registro_exitoso': True,  # Indicador de registro exitoso
            })
        else:
            # Si el formulario de apoderado no es válido, se vuelve a mostrar con los errores
            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'alumno_form': alumno_form,
                'apoderado_form': apoderado_form,
                'show_apoderado_form': True,  # Mostrar formulario de apoderado
                'show_alumno_form': False,    # Ocultar formulario de alumno
            })

    return render(request, 'ingApp/index.html', {
        'section': 'matricula',
        'alumno_form': alumno_form,
        'apoderado_form': apoderado_form,
        'show_apoderado_form': False,  # No mostrar formulario de apoderado
        'show_alumno_form': True,     # Mostrar formulario de alumno
    })

@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()  # Obtener todos los alumnos
    return render(request, 'ingApp/lista_alumnos.html', {'alumnos': alumnos})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm
