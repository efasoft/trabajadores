from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Any
from datetime import date
import re
from django.core.exceptions import ValidationError

class TrabajadorModel(BaseModel):
    nombres: str
    apellidos: str
    edad: int
    fecha: date
    email: EmailStr
    telefono_casa: str
    telefono_movil: str
    sueldo_base: float
    comision: float
    password: str
    foto: Any  # <-- CAMBIO HECHO AQUÍ
    activo: bool = True
    provincia: Any   # Nuevo campo
    ciudad: Any      # Nuevo campo
    codigo_postal: str  # Nuevo campo    

    # --- Nombres / Apellidos ---
    @field_validator('nombres')
    def nombre_max_length(cls, v):
        if len(v) > 60:
            raise ValueError('Máximo 60 caracteres')
        return v

    @field_validator('apellidos')
    def nombre_vacio_length(cls, v):
        if not v:
            raise ValueError('Este campo no puede quedar vacío')
        return v

    # --- Edad ---
    @field_validator('edad')
    def edad_valida(cls, v):
        if not (18 <= v <= 100):
            raise ValueError('Edad debe estar entre 18 y 100')
        return v

    # --- Fecha ---
    @field_validator('fecha')
    def validar_fecha(cls, v):
        if not isinstance(v, date):
           raise ValueError("Fecha inválida. Usa el formato DD/MM/AAAA")
        if v > date.today():
           raise ValueError("La fecha no puede ser futura")
        if not v:
            raise ValueError('Debe ingresar una fecha')       
        return v       

    # --- Teléfonos ---
    @field_validator('telefono_casa')
    def validar_telefono_casa(cls, v):
        if not re.match(r'^9[0-9]{8}$', v):
            raise ValueError("Teléfono fijo inválido (Ej: 912345678)")
        return v

    @field_validator('telefono_movil')
    def validar_telefono_movil(cls, v):
        if not re.match(r'^6[0-9]{8}$', v):
            raise ValueError("Teléfono móvil inválido (Ej: 612345678)")
        return v

    # --- Sueldos ---
    @field_validator('sueldo_base', 'comision')
    def validar_montos(cls, v):
        if v < 0:
            raise ValueError('Valor no puede ser negativo')
        return v

    # --- Password ---
    @field_validator('password')
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError('Atención: Contraseña mínima de 8 caracteres')
        return v

    # --- Foto ---
    @field_validator('foto')
    def validar_foto(cls, v):
        if not v:
            raise ValueError('Debe subir una imagen')
        if hasattr(v, 'name') and not v.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError('Formato de imagen inválido (JPG o PNG requeridos)')
        return v

    # --- Provincia ---
    @field_validator('provincia')
    def validar_provincia(cls, v):
        if not v:
            raise ValueError("Debe seleccionar una provincia")
        return v

    # --- Ciudad ---
    @field_validator('ciudad')
    def validar_ciudad(cls, v):
        if not v:
            raise ValueError("Debe seleccionar una ciudad")
        return v

    # --- Código Postal ---
    @field_validator('codigo_postal')
    def validar_codigo_postal(cls, v):
        if not re.match(r'^[0-9]{4,10}$', v):
            raise ValueError("Código Postal inválido (solo números, entre 4 y 10 dígitos)")
        return v    

    # --- Sueldo Bruto Validado ---
    @model_validator(mode="after")
    def calcular_sueldo_bruto(self):
        if (self.sueldo_base + self.comision) <= 0:
            raise ValueError("El sueldo bruto debe ser mayor que cero")
        return self
    
# =========================
#   Provincia Model
# =========================
class ProvinciaModel(BaseModel):
    nombre: str

    @field_validator("nombre")
    def nombre_valido(cls, v):
        if len(v) > 60:
            raise ValueError("Máximo 60 caracteres")
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return v


# =========================
#   Ciudad Model
# =========================
class CiudadModel(BaseModel):
    nombre: str
    provincia: int  # Puede ser un ID de Provincia

    @field_validator("nombre")
    def nombre_valido(cls, v):
        if len(v) > 60:
            raise ValueError("Máximo 60 caracteres")
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not v.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return v



# Validadores auxiliares (para forms.py clásicos)
def validar_telefono(value):
    if not value.isdigit() or len(value) < 7:
        raise ValidationError("El número telefónico debe contener al menos 7 dígitos numéricos.")

def validar_nombre(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("El nombre solo debe contener letras.")


