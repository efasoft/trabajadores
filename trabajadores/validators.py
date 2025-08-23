# validators.py
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Any
from datetime import date
import re


class TrabajadorModel(BaseModel):
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }

    nombres: str
    apellidos: str
    edad: int
    fecha: str
    email: EmailStr
    telefono_casa: str
    telefono_movil: str
    sueldo_base: float
    comision: float
    password: str
    foto: Any
    activo: bool = True
    provincia: int
    ciudad: int
    codigo_postal: str

    @field_validator('nombres')
    def validar_nombres(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un nombre")
        if len(v) > 60:
            raise ValueError("El nombre no puede superar 60 caracteres")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return v

    @field_validator('apellidos')
    def validar_apellidos(cls, v):
        if not v or not v.strip():
            raise ValueError("Debe ingresar un apellido")
        if len(v) > 60:
            raise ValueError("El apellido no puede superar 60 caracteres")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El apellido solo debe contener letras")
        return v

    @field_validator('edad')
    def validar_edad(cls, v):
        if v is None:
            raise ValueError("Debe ingresar la edad")
        if not isinstance(v, int):
            raise ValueError("La edad debe ser un número entero")
        if v < 18:
            raise ValueError("La edad mínima es 18 años")
        if v > 100:
            raise ValueError("La edad máxima es 100 años")
        return v

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
        if not isinstance(v, str):
            raise ValueError("El teléfono fijo debe ser un número válido")
        if not re.match(r'^9[0-9]{8}$', v):
            raise ValueError("Teléfono fijo inválido (Ej: 912345678)")
        return v

    @field_validator('telefono_movil')
    def validar_telefono_movil(cls, v):
        if not isinstance(v, str):
            raise ValueError("El teléfono móvil debe ser un número válido")
        if not re.match(r'^6[0-9]{8}$', v):
            raise ValueError("Teléfono móvil inválido (Ej: 612345678)")
        return v

    @field_validator('sueldo_base')
    def validar_sueldo_base(cls, v):
        if v is None:
            raise ValueError("Debe ingresar el sueldo base")
        if not isinstance(v, (int, float)):
            raise ValueError("El sueldo base debe ser un número")
        if v < 0:
            raise ValueError("El sueldo base no puede ser negativo")
        if v > 1_000_000:
            raise ValueError("El sueldo base no puede ser mayor a 1.000.000 €")
        return round(float(v), 2)

    @field_validator('comision')
    def validar_comision(cls, v):
        if v is None:
            raise ValueError("Debe ingresar la comisión")
        if not isinstance(v, (int, float)):
            raise ValueError("La comisión debe ser un número")
        if v < 0:
            raise ValueError("La comisión no puede ser negativa")
        if v > 500_000:
            raise ValueError("La comisión no puede ser mayor a 500.000 €")
        return round(float(v), 2)

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
        if not v:
            raise ValueError("Debe seleccionar una provincia")
        if not isinstance(v, int):
            raise ValueError("La provincia seleccionada no es válida")
        return v

    @field_validator('ciudad')
    def validar_ciudad(cls, v):
        if not v:
            raise ValueError("Debe seleccionar una ciudad")
        if not isinstance(v, int):
            raise ValueError("La ciudad seleccionada no es válida")
        return v

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


  



