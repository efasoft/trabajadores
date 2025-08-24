# validators.py
from typing import Any, Optional
from pydantic import BaseModel, field_validator, model_validator
import re


class TrabajadorModel(BaseModel):
    """
    Modelo Pydantic para validar los datos del formulario Trabajador.
    Todos los campos deben cumplir con reglas específicas en español.
    """
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }

    # Campos obligatorios
    nombres: str
    apellidos: str

    # Campos opcionales (pueden ser None o cadena vacía)
    edad: Optional[str] = None
    fecha: Optional[str] = None
    email: Optional[str] = None
    telefono_casa: Optional[str] = None
    telefono_movil: Optional[str] = None
    sueldo_base: Optional[str] = None
    comision: Optional[str] = None
    password: Optional[str] = None
    foto: Any  # Validado manualmente
    activo: bool = True
    provincia: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None

    # Validadores de campo

    @field_validator('nombres')
    def validar_nombres(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un nombre")
        if len(v) > 60:
            raise ValueError("El nombre no puede superar 60 caracteres")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return v.strip()

    @field_validator('apellidos')
    def validar_apellidos(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un apellido")
        if len(v) > 60:
            raise ValueError("El apellido no puede superar 60 caracteres")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El apellido solo debe contener letras")
        return v.strip()

    @field_validator('edad')
    def validar_edad(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar la edad")
        if not v.isdigit():
            raise ValueError("La edad debe ser un número entero")
        v_int = int(v)
        if v_int < 18:
            raise ValueError("La edad mínima es 18 años")
        if v_int > 100:
            raise ValueError("La edad máxima es 100 años")
        return v_int

    @field_validator('fecha')
    def validar_fecha(cls, v):
        from datetime import datetime
        if not v:
            raise ValueError("Debe ingresar una fecha")
        try:
            datetime.strptime(v, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError("Fecha inválida. Usa el formato DD/MM/AAAA")
        return v

    @field_validator('email')
    def validar_email(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un correo electrónico")
        v = v.strip()
        if len(v) > 254:
            raise ValueError("El correo no puede superar 254 caracteres")
        if '@' not in v:
            raise ValueError("El correo debe contener '@'")
        if v.count('@') != 1:
            raise ValueError("El correo solo debe tener un '@'")
        nombre, dominio = v.rsplit('@', 1)
        if not nombre:
            raise ValueError("El correo debe tener un nombre antes de '@'")
        if not dominio or '.' not in dominio:
            raise ValueError("El dominio del correo no es válido")
        if dominio.startswith('.') or dominio.endswith('.'):
            raise ValueError("El dominio no puede empezar ni terminar con '.'")
        if '..' in dominio:
            raise ValueError("El dominio no puede contener '..'")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Correo electrónico inválido")
        return v

    @field_validator('telefono_casa')
    def validar_telefono_casa(cls, v):
        if not v or not v.strip():
            raise ValueError("El teléfono fijo debe ser un número válido")
        v = v.strip()
        if not re.match(r'^9[0-9]{8}$', v):
            raise ValueError("Teléfono fijo inválido (Ej: 912345678)")
        return v

    @field_validator('telefono_movil')
    def validar_telefono_movil(cls, v):
        if not v or not v.strip():
            raise ValueError("El teléfono móvil debe ser un número válido")
        v = v.strip()
        if not re.match(r'^6[0-9]{8}$', v):
            raise ValueError("Teléfono móvil inválido (Ej: 612345678)")
        return v

    @field_validator('sueldo_base')
    def validar_sueldo_base(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar el sueldo base")
        try:
            v_float = float(v)
        except ValueError:
            raise ValueError("El sueldo base debe ser un número")
        if v_float < 0:
            raise ValueError("El sueldo base no puede ser negativo")
        if v_float > 1_000_000:
            raise ValueError("El sueldo base no puede ser mayor a 1.000.000 €")
        return round(v_float, 2)

    @field_validator('comision')
    def validar_comision(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar la comisión")
        try:
            v_float = float(v)
        except ValueError:
            raise ValueError("La comisión debe ser un número")
        if v_float < 0:
            raise ValueError("La comisión no puede ser negativa")
        if v_float > 500_000:
            raise ValueError("La comisión no puede ser mayor a 500.000 €")
        return round(v_float, 2)

    @field_validator('password')
    def validar_password(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar una contraseña")
        v = v.strip()
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v) > 128:
            raise ValueError("La contraseña no puede superar 128 caracteres")
        return v

    @field_validator('foto')
    def validar_foto(cls, v):
        if not v:
            raise ValueError("Debe subir una imagen")
        if hasattr(v, 'name') and not v.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError("Formato de imagen inválido (JPG o PNG requeridos)")
        return v

    @field_validator('provincia')
    def validar_provincia(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe seleccionar una provincia")
        if not v.isdigit():
            raise ValueError("La provincia seleccionada no es válida")
        return int(v)

    @field_validator('ciudad')
    def validar_ciudad(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe seleccionar una ciudad")
        if not v.isdigit():
            raise ValueError("La ciudad seleccionada no es válida")
        return int(v)

    @field_validator('codigo_postal')
    def validar_codigo_postal(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un código postal")
        v = v.strip()
        if not re.match(r'^[0-9]{4,10}$', v):
            raise ValueError("Código Postal inválido (solo números, entre 4 y 10 dígitos)")
        return v

    @model_validator(mode="after")
    def calcular_sueldo_bruto(cls, model):
        total = model.sueldo_base + model.comision
        if total <= 0:
            raise ValueError("El sueldo bruto debe ser mayor que cero")
        return model
  



