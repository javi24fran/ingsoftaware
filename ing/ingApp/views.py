from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from ingApp.forms import AlumnoForm, ApoderadoForm
from ingApp.models import Alumno, Apoderado
from django.db import transaction
from django.db.models import Q

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
                'apoderado_form': ApoderadoForm(),  
                'show_apoderado_form': True, 
                'show_alumno_form': False,  
            })
        else:
            # Si el formulario de alumno no es válido
            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'alumno_form': alumno_form,
                'apoderado_form': apoderado_form,
                'show_apoderado_form': False, 
                'show_alumno_form': True,     
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

                #asociar el apoderado con el alumno en la relación inversa
                alumno.apoderado = apoderado
                alumno.save()


                del request.session['alumno_data']


            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'apoderado_form': apoderado_form,
                'show_apoderado_form': False,
                'show_alumno_form': False,
                'registro_exitoso': True,  
            })
        else:

            return render(request, 'ingApp/index.html', {
                'section': 'matricula',
                'alumno_form': alumno_form,
                'apoderado_form': apoderado_form,
                'show_apoderado_form': True, 
                'show_alumno_form': False,    
            })

    return render(request, 'ingApp/index.html', {
        'section': 'matricula',
        'alumno_form': alumno_form,
        'apoderado_form': apoderado_form,
        'show_apoderado_form': False,  
        'show_alumno_form': True,     
    })


@login_required
def lista_alumnos(request):
    # Obtener el término de búsqueda de la solicitud GET
    query = request.GET.get('search', '').strip()  # Elimina espacios al inicio y final
    if query:
        # Filtrar alumnos por nombre o apellido (contiene, no sensible a mayúsculas)
        alumnos = Alumno.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query)
        )
    else:
        # Si no hay búsqueda, mostrar todos los alumnos
        alumnos = Alumno.objects.all()

    # Pasar los resultados y el término de búsqueda a la plantilla
    return render(request, 'ingApp/lista_alumnos.html', {
        'alumnos': alumnos,
        'search': query  # Para mostrar el término en el campo de búsqueda
    })

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

@login_required
def detalle_alumno(request, alumno_id):
    
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    return render(request, 'ingApp/detalle-alumno.html', {
        'alumno': alumno
    })

@login_required
def actualizar_alumno(request, alumno_id):
    # Obtén el alumno o muestra un error 404 si no existe
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    apoderado = get_object_or_404(Apoderado, pk= alumno_id)

    # Si el formulario es enviado (método POST), procesa los datos
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST, instance=alumno)  # Prellena con el alumno existente
        apoderado_form = ApoderadoForm(request.POST, instance=apoderado)
        if alumno_form.is_valid():
            alumno_form.save()  # Guarda los cambios
            apoderado_form.save()
            messages.success(request, 'Los datos del alumno se han actualizado exitosamente.')
            return redirect('detalle_alumno', alumno_id=alumno.id)  # Redirige al detalle del alumno
    else:
        # Si no es POST, muestra el formulario con los datos actuales
        alumno_form = AlumnoForm(instance=alumno)
        apoderado_form = ApoderadoForm(instance=apoderado)

    return render(request, 'ingApp/actualizar_alumno.html', {
        'alumno_form': alumno_form, 'apoderado_form': apoderado_form,
        'alumno': alumno  # Pasamos el objeto alumno por si es necesario en el template


    })

@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)  # Obtén el alumno a eliminar
    alumno.delete()  # Elimina el alumno de la base de datos
    messages.success(request, 'El alumno ha sido eliminado exitosamente.')
    return redirect('lista_alumnos')  # Redirige a la lista de alumnos
