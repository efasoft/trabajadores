# trabajadores/tests.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import TrabajadorForm
from .models import Provincia, Ciudad


class ValidacionTrabajadorTest(TestCase):
    """
    Pruebas exhaustivas para TrabajadorForm.
    Verifica que todos los errores se muestren en español.
    """

    @classmethod
    def setUpTestData(cls):
        # Crear datos base
        cls.provincia = Provincia.objects.create(nombre="Madrid")
        cls.ciudad = Ciudad.objects.create(nombre="Madrid", provincia=cls.provincia)

        # Archivo simulado para 'foto'
        cls.foto = SimpleUploadedFile(
            name="test_foto.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )

    def _get_datos_base(self):
        """Retorna un diccionario con datos válidos por defecto"""
        return {
            "nombres": "Juan",
            "apellidos": "Pérez",
            "fecha": "01/01/1990",
            "telefono_casa": "912345678",
            "telefono_movil": "612345678",
            "sueldo_base": "1000.00",
            "comision": "200.00",
            "password": "micontraseña123",
            "provincia": str(self.provincia.id),
            "ciudad": str(self.ciudad.id),
            "codigo_postal": "28001",
            "activo": "on",
            "edad": "30",
            "correo": "juan@perez.com"
        }

    def _form_errors(self, datos):
        """
        Helper: Retorna los errores del formulario como string.
        Asegura que se envíe 'foto' en todas las pruebas.
        """
        form = TrabajadorForm(data=datos, files={"foto": self.foto})
        form.is_valid()
        return str(form.errors)

    # --- NOMBRES ---
    def test_nombres_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["nombres"] = ""
        self.assertIn("Debe ingresar un nombre", self._form_errors(datos))

    def test_nombres_demasiado_largo_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["nombres"] = "A" * 61
        self.assertIn("El nombre no puede superar 60 caracteres", self._form_errors(datos))

    def test_nombres_con_numeros_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["nombres"] = "Juan123"
        self.assertIn("El nombre solo debe contener letras", self._form_errors(datos))

    # --- APELLIDOS ---
    def test_apellidos_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["apellidos"] = ""
        self.assertIn("Debe ingresar un apellido", self._form_errors(datos))

    def test_apellidos_demasiado_largo_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["apellidos"] = "A" * 61
        self.assertIn("El apellido no puede superar 60 caracteres", self._form_errors(datos))

    def test_apellidos_con_numeros_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["apellidos"] = "Pérez123"
        self.assertIn("El apellido solo debe contener letras", self._form_errors(datos))

    # --- FECHA ---
    def test_fecha_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["fecha"] = ""
        self.assertIn("Debe ingresar una fecha", self._form_errors(datos))

    def test_fecha_formato_invalido_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["fecha"] = "01-01-1990"
        self.assertIn("Fecha inválida. Usa el formato DD/MM/AAAA", self._form_errors(datos))

    # --- CORREO ---
    def test_correo_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["correo"] = ""
        self.assertIn("Debe ingresar un correo electrónico", self._form_errors(datos))

    def test_correo_sin_arroba_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["correo"] = "usuarioexample.com"
        error_html = self._form_errors(datos)
        self.assertIn("El correo debe contener", error_html)
        self.assertIn("@", error_html)

    def test_correo_doble_arroba_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["correo"] = "usuario@@example.com"
        error_html = self._form_errors(datos)
        self.assertIn("El correo solo debe tener", error_html)
        self.assertIn("@", error_html)

    def test_correo_sin_nombre_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["correo"] = "@example.com"
        error_html = self._form_errors(datos)
        self.assertIn("El correo debe tener un nombre antes de", error_html)
        self.assertIn("@", error_html)

    def test_correo_sin_dominio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["correo"] = "usuario@"
        self.assertIn("El dominio del correo no es válido", self._form_errors(datos))

    # --- EDAD ---
    def test_edad_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["edad"] = ""
        self.assertIn("Debe ingresar la edad", self._form_errors(datos))

    def test_edad_no_numerica_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["edad"] = "abc"
        self.assertIn("La edad debe ser un número entero", self._form_errors(datos))

    def test_edad_menor_que_18_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["edad"] = "17"
        self.assertIn("La edad mínima es 18 años", self._form_errors(datos))

    def test_edad_mayor_que_100_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["edad"] = "101"
        self.assertIn("La edad máxima es 100 años", self._form_errors(datos))

    # --- TELÉFONO CASA ---
    def test_telefono_casa_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_casa"] = ""
        self.assertIn("El teléfono fijo debe ser un número válido", self._form_errors(datos))

    def test_telefono_casa_no_numerico_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_casa"] = "abcdefghi"
        self.assertIn("Teléfono fijo inválido (Ej: 912345678)", self._form_errors(datos))

    def test_telefono_casa_formato_invalido_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_casa"] = "812345678"
        self.assertIn("Teléfono fijo inválido (Ej: 912345678)", self._form_errors(datos))

    # --- TELÉFONO MÓVIL ---
    def test_telefono_movil_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_movil"] = ""
        self.assertIn("El teléfono móvil debe ser un número válido", self._form_errors(datos))

    def test_telefono_movil_no_numerico_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_movil"] = "abcdefghi"
        self.assertIn("Teléfono móvil inválido (Ej: 612345678)", self._form_errors(datos))

    def test_telefono_movil_formato_invalido_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["telefono_movil"] = "512345678"
        self.assertIn("Teléfono móvil inválido (Ej: 612345678)", self._form_errors(datos))

    # --- SUELDO BASE ---
    def test_sueldo_base_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["sueldo_base"] = ""
        self.assertIn("Debe ingresar el sueldo base", self._form_errors(datos))

    def test_sueldo_base_no_numerico_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["sueldo_base"] = "abc"
        self.assertIn("El sueldo base debe ser un número", self._form_errors(datos))

    def test_sueldo_base_negativo_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["sueldo_base"] = "-100"
        self.assertIn("El sueldo base no puede ser negativo", self._form_errors(datos))

    def test_sueldo_base_demasiado_alto_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["sueldo_base"] = "1000001"
        self.assertIn("El sueldo base no puede ser mayor a 1.000.000 €", self._form_errors(datos))

    # --- COMISIÓN ---
    def test_comision_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["comision"] = ""
        self.assertIn("Debe ingresar la comisión", self._form_errors(datos))

    def test_comision_no_numerica_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["comision"] = "abc"
        self.assertIn("La comisión debe ser un número", self._form_errors(datos))


    # --- PASSWORD ---
    def test_password_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["password"] = ""
        self.assertIn("Debe ingresar una contraseña", self._form_errors(datos))

    def test_password_corto_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["password"] = "1234567"
        self.assertIn("La contraseña debe tener al menos 8 caracteres", self._form_errors(datos))

    def test_password_demasiado_largo_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["password"] = "A" * 129
        self.assertIn("La contraseña no puede superar 128 caracteres", self._form_errors(datos))

    # --- FOTO ---
    def test_foto_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        form = TrabajadorForm(data=datos, files={})
        form.is_valid()
        self.assertIn("Debe subir una imagen", str(form.errors))

    def test_foto_formato_invalido_muestra_error_espanol(self):
        foto_invalida = SimpleUploadedFile("test.txt", b"content", content_type="text/plain")
        datos = self._get_datos_base()
        form = TrabajadorForm(data=datos, files={"foto": foto_invalida})
        form.is_valid()
        self.assertIn("Formato de imagen inválido (JPG o PNG requeridos)", str(form.errors))

    # --- PROVINCIA ---
    def test_provincia_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["provincia"] = ""
        self.assertIn("Debe seleccionar una provincia", self._form_errors(datos))

    def test_provincia_no_numerica_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["provincia"] = "abc"
        self.assertIn("La provincia seleccionada no es válida", self._form_errors(datos))

    # --- CIUDAD ---
    def test_ciudad_vacia_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["ciudad"] = ""
        self.assertIn("Debe seleccionar una ciudad", self._form_errors(datos))

    def test_ciudad_no_numerica_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["ciudad"] = "abc"
        self.assertIn("La ciudad seleccionada no es válida", self._form_errors(datos))

    # --- CÓDIGO POSTAL ---
    def test_codigo_postal_vacio_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["codigo_postal"] = ""
        self.assertIn("Debe ingresar un código postal", self._form_errors(datos))

    def test_codigo_postal_no_numerico_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["codigo_postal"] = "abcde"
        self.assertIn("Código Postal inválido (solo números, entre 4 y 10 dígitos)", self._form_errors(datos))

    def test_codigo_postal_demasiado_corto_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["codigo_postal"] = "123"
        self.assertIn("Código Postal inválido (solo números, entre 4 y 10 dígitos)", self._form_errors(datos))

    def test_codigo_postal_demasiado_largo_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["codigo_postal"] = "12345678901"
        self.assertIn("Código Postal inválido (solo números, entre 4 y 10 dígitos)", self._form_errors(datos))

    # --- SUELDO BRUTO ---
    def test_sueldo_bruto_cero_muestra_error_espanol(self):
        datos = self._get_datos_base()
        datos["sueldo_base"] = "0"
        datos["comision"] = "0"
        self.assertIn("El sueldo bruto debe ser mayor que cero", self._form_errors(datos))
