from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime
import re

class TrabajadorSchema(BaseModel):
    nombres: str = Field(..., max_length=60)
    apellidos: str = Field(..., max_length=60)
    edad: int = Field(..., le=100)
    fecha: str
    email: EmailStr
    telefono_casa: str
    telefono_movil: str
    sueldo_base: str
    comision: str
    password: str = Field(..., min_length=8)

    @field_validator('fecha')
    def validar_fecha(cls, v):
        try:
            datetime.strptime(v, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Usa DD-MM-AAAA")
        return v

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

    @field_validator('sueldo_base', 'comision')
    def validar_dinero(cls, v):
        if not re.match(r'^\d{1,3}(?:\.\d{3})*,\d{2}$', v):
            raise ValueError("Formato de sueldo inválido. Usa separador de miles y decimales con coma")
        return v

    @model_validator(mode='after')
    def check_all_fields(self):
        if not self.nombres or not self.apellidos:
            raise ValueError("Todos los campos son obligatorios")
        return self
