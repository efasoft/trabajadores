from django.db import models

class Trabajador(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono_movil = models.CharField(max_length=15)
    telefono_casa = models.CharField(max_length=15, blank=True, null=True)
    edad = models.PositiveIntegerField()
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    activo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos_trabajadores/', blank=True, null=True)
    password = models.CharField(max_length=128)

    @property
    def sueldo_bruto(self):
        return (self.sueldo_base or 0) + (self.comision or 0)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"






