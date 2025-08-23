# trabajadores/tests.py
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import TrabajadorForm
from .models import Provincia, Ciudad


class ValidacionTrabajadorTest(TestCase):
    def setUp(self):
        # Crear datos básicos necesarios
        self.provincia = Provincia.objects.create(nombre="Madrid")
        self.ciudad = Ciudad.objects.create(nombre="Madrid", provincia=self.provincia)

    def test_validaciones_mensajes_espanol(self):
        """
        Verifica que todos los errores se muestren en español
        """
        casos = [
            # email
            (
                {
                    "email": "",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Debe ingresar un correo electrónico"
            ),
            (
                {
                    "email": "usuario@",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "El dominio del correo no es válido"
            ),
            (
                {
                    "email": "usuario@dominio",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Correo electrónico inválido"
            ),

            # edad
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Debe ingresar la edad"
            ),
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "17",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "La edad mínima es 18 años"
            ),
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "abc",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "La edad debe ser un número entero"
            ),

            # sueldo_base
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "-100",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "El sueldo base no puede ser negativo"
            ),
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Debe ingresar el sueldo base"
            ),

            # comision
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "-50",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "La comisión no puede ser negativa"
            ),

            # password
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "123",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "La contraseña debe tener al menos 8 caracteres"
            ),
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Debe ingresar una contraseña"
            ),

            # provincia
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": "",
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "28001"
                },
                "Debe seleccionar una provincia"
            ),

            # ciudad
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": "",
                    "codigo_postal": "28001"
                },
                "Debe seleccionar una ciudad"
            ),

            # codigo_postal
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": ""
                },
                "Debe ingresar un código postal"
            ),
            (
                {
                    "email": "valido@dominio.com",
                    "edad": "25",
                    "sueldo_base": "1000",
                    "comision": "200",
                    "password": "12345678",
                    "provincia": str(self.provincia.id),
                    "ciudad": str(self.ciudad.id),
                    "codigo_postal": "abc"
                },
                "Código Postal inválido (solo números, entre 4 y 10 dígitos)"
            ),
        ]

        print("\n" + "="*80)
        print("🧪 INICIO DE PRUEBAS - VALIDACIONES EN ESPAÑOL")
        print("="*80)

        for i, (datos, mensaje_esperado) in enumerate(casos, 1):
            with self.subTest(caso=i):
                form = TrabajadorForm(data=datos)
                self.assertFalse(form.is_valid(), f"Formulario inesperadamente válido: {datos}")

                # Buscar el mensaje esperado en cualquier campo
                errores = []
                for field in form:
                    for error in field.errors:
                        errores.append(str(error))

                self.assertTrue(
                    any(mensaje_esperado in error for error in errores),
                    f"No se encontró el mensaje esperado: '{mensaje_esperado}'. Obtenido: {errores}"
                )
                print(f"✅ [Prueba {i}] OK - '{mensaje_esperado}'")

        print("="*80)
        print("🎉 ¡Todas las validaciones muestran mensajes en español!")
        print("="*80)


