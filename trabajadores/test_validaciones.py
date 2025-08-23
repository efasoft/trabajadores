# test_validaciones.py
from trabajadores.forms import TrabajadorForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os

# Simulación de datos inválidos para probar cada validación
casos_de_prueba = [
    # Campo: email
    {
        "datos": {
            "email": "",
            "edad": "25",
            "sueldo_base": "1000",
            "comision": "200",
            "password": "12345678",
            "provincia": "1",
            "ciudad": "1",
            "codigo_postal": "28001"
        },
        "esperado": "Debe ingresar un correo electrónico"
    },
    {
        "datos": {
            "email": "usuario@",
            "edad": "25",
            "sueldo_base": "1000",
            "comision": "200",
            "password": "12345678",
            "provincia": "1",
            "ciudad": "1",
            "codigo_postal": "28001"
        },
        "esperado": "El dominio del correo no es válido"
    },
    # ... (el resto de los casos igual)
]

# Ejecutar pruebas
def ejecutar_pruebas():
    print("=" * 80)
    print("🧪 INICIO DE PRUEBAS DE VALIDACIÓN - MENSAJES EN ESPAÑOL")
    print("=" * 80)

    fallos = 0
    exitos = 0

    for i, caso in enumerate(casos_de_prueba, 1):
        datos = caso["datos"]
        esperado = caso["esperado"]

        # Crear formulario
        form = TrabajadorForm(datos)

        # Validar
        if form.is_valid():
            print(f"❌ [Prueba {i}] ❌ Formulario válido cuando no debería serlo")
            fallos += 1
            continue

        # Obtener todos los errores
        errores = []
        for field in form:
            for error in field.errors:
                errores.append(str(error))

        # Verificar que el mensaje esperado esté presente
        encontrado = any(esperado in err for err in errores)

        if encontrado:
            print(f"✅ [Prueba {i}] OK - Mensaje correcto: '{esperado}'")
            exitos += 1
        else:
            print(f"❌ [Prueba {i}] ❌ Esperado: '{esperado}' | Obtenido: {errores}")
            fallos += 1

    print("=" * 80)
    print(f"✅ Éxitos: {exitos}")
    print(f"❌ Fallos: {fallos}")
    print("=" * 80)

    if fallos == 0:
        print("🎉 ¡Todas las validaciones muestran mensajes en español correctamente!")
    else:
        print("⚠️  Algunas validaciones no muestran los mensajes esperados. Revisa los archivos.")

# Ejecutar
if __name__ == "__main__":
    import django
    import os

    # Configurar Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # ← Cambia "myproject" por tu carpeta de settings
    django.setup()

    ejecutar_pruebas()