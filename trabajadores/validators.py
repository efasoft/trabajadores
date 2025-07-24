from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import date
import re

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
    foto: str
    activo: bool = True

    @field_validator('nombres', 'apellidos')
    def nombre_max_length(cls, v):
        if len(v) > 60:
            raise ValueError('Máximo 60 caracteres')
        return v

    @field_validator('edad')
    def edad_valida(cls, v):
        if not (18 <= v <= 100):
            raise ValueError('Atención : Edad debe estar entre 18 y 100')
        return v

    @field_validator('telefono_casa')
    def validar_telefono_casa(cls, v):
        if not re.match(r'^\\d{9}$', v):
            raise ValueError('Teléfono casa inválido')
        return v

    @field_validator('telefono_movil')
    def validar_telefono_movil(cls, v):
        if not re.match(r'^6\\d{8}$', v):
            raise ValueError('Teléfono móvil inválido')
        return v

    @field_validator('sueldo_base', 'comision')
    def validar_montos(cls, v):
        if v < 0:
            raise ValueError('Valor no puede ser negativo')
        return v

    @field_validator('password')
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError('Atención : Contraseña mínima de 8 caracteres')
        return v

    @field_validator('foto')
    def validar_foto(cls, v):
        if not v:
            raise ValueError('Debe subir una imagen')
        return v

    @model_validator(mode="after")
    def calcular_sueldo_bruto(self):
        if (self.sueldo_base + self.comision) <= 0:
            raise ValueError("El sueldo bruto debe ser mayor que cero")
        return self


