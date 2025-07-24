from django.db import models

class Trabajador(models.Model):
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    edad = models.PositiveIntegerField()
    fecha = models.DateField()
    email = models.EmailField()
    telefono_casa = models.CharField(max_length=9)
    telefono_movil = models.CharField(max_length=9)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    password = models.CharField(max_length=128)
    foto = models.ImageField(upload_to='trabajadores_fotos/')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def sueldo_bruto(self):
      if self.sueldo_base is None or self.comision is None:
          return 0
      return self.sueldo_base + self.comision




