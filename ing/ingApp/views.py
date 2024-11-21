from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from ingApp.forms import AlumnoForm
from ingApp.models import Alumno


@login_required
def index(request):
    return render(request,'ingApp/index.html')

@login_required
def matricula_view(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save() 
            form = AlumnoForm()  
    else:
        form = AlumnoForm()
    return render(request, 'ingApp/index.html', {'form': form, 'section': 'matricula'})

@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()  # Obtener todos los alumnos
    return render(request, 'ingApp/lista_alumnos.html', {'alumnos': alumnos})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm
