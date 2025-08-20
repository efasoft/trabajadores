from django.db import models

class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name="ciudades")
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ('provincia', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"


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

    # NUEVOS CAMPOS
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)

    @property
    def sueldo_bruto(self):
        return (self.sueldo_base or 0) + (self.comision or 0)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
