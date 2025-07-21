from django.db import models
from django.contrib.auth.hashers import make_password

class Trabajador(models.Model):
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    edad = models.PositiveIntegerField()
    fecha = models.DateField()
    email = models.EmailField(unique=True)
    telefono_casa = models.CharField(max_length=15)
    telefono_movil = models.CharField(max_length=15)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    sueldo_bruto = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    password = models.CharField(max_length=128)
    foto = models.ImageField(upload_to='fotos/')
    eliminado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.sueldo_bruto = self.sueldo_base + self.comision
        if not self.pk or 'password' in self.get_deferred_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
