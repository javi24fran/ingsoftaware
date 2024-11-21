from django.db import models

class Alumno(models.Model):
    # Campos para los datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    # Etnia (Sí o No) con opciones
    ETNIA_CHOICES = [
        ('Si', 'Sí'),
        ('No', 'No'),
    ]
    etnia = models.CharField(
        max_length=3,
        choices=ETNIA_CHOICES,
        default='No'
    )
    
    # Número de emergencia
    numero_emergencia = models.CharField(max_length=15)
    
    # Colegio de procedencia
    colegio_procedencia = models.CharField(max_length=200)
    
    # Beneficios JUNAEB
    BENEFICIOS_CHOICES = [
        ('Beca_baes', 'Beca de Alimentación Escolar'),
        ('Beca_enseñanza', 'Beca de Enseñanza Media'),
        ('Beca_presidente', 'Beca Presidente de la República'),
        ('Ninguno', 'Ninguno'),
    ]
    beneficio_junaeb = models.CharField(
        max_length=20, 
        choices=BENEFICIOS_CHOICES, 
        default='Ninguno'
    )
    
    # Sistema de salud
    SISTEMA_SALUD_CHOICES = [
        ('Fonasa', 'Fonasa'),
        ('Isapre', 'Isapre'),
        ('Privado', 'Salud Privada'),
        ('Ninguno', 'Sin Sistema de Salud'),
    ]
    sistema_salud = models.CharField(
        max_length=20,
        choices=SISTEMA_SALUD_CHOICES,
        default='Ninguno'
    )
    
    # Fecha de creación del registro
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

